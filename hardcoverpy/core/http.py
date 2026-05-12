import os
import json
import logging

import urllib3
from urllib3.exceptions import HTTPError

__all__ = ('HardcoverEndpoint', 'endpoint_url')

endpoint_url = "https://api.hardcover.app/v1/graphql"

class BaseEndpoint:
  def __call__(self):
    raise NotImplementedError()

class HardcoverEndpoint(BaseEndpoint):
  '''
    GraphQL access done over HTTP using urllib3. (This is a modified version of the `sgqlc` )
  '''
  logger = logging.getLogger(__name__)
  def __init__(
    self,
    base_headers: dict = None,
    method: str = 'POST',
    # url: str = os.environ['API_URL'] or "https://api.hardcover.app/v1/graphql",
    url: str = "https://api.hardcover.app/v1/graphql",
    timeout: int = 30,
    urlopen = None,
  ):
    self.base_headers = base_headers or {}
    self.method = method
    self.url = url
    self.timeout = timeout
    self.urlopen = urlopen or urllib3.HTTPConnectionPool.urlopen
  
  def __str__(self):
    return '%s(url=%s, base_headers=%s, timeout=%s, method=%s)' % (
      self.__class__.__name__,
      self.url,
      self.base_headers,
      self.timeout,
      self.method
    )

  def _prepare(
    self,
    query,
    variables,
    operation_name
  ):
    if isinstance(query, bytes):
      query = query.decode('utf-8')
    elif not isinstance(query, str):
      query = bytes(query).decode('utf-8')
    
    headers = self.base_headers.copy()
    if 'content-type' not in headers:
      content_type = {'content-type': 'application/json'}
      headers.update(content_type)
    if 'Accept' not in headers:
      accept = {'Accept': 'application/graphql-response+json;charset=utf-8,application/json;charset=utf-8'}
      headers.update(accept)
    
    req = self.get_request(query, variables, operation_name, headers)
    return query, req


  def __call__(self, query, variables=None, operation_name=None):
    query, req = self._prepare(
      query=query,
      variables=variables,
      operation_name=operation_name
    )

    self.logger.debug('Query:\n%s', query)

    try:
      with self.urlopen(method=self.method, url=self.url, timeout=self.timeout) as f:
        headers = f.headers
        content_encoding = headers.get('Content-Encoding')
        if content_encoding and 'gzip' in content_encoding:
          import gzip
          content = gzip.decompress(f.read())
          del headers['Content-Encoding']
        else:
          content = f.read()
        body = content.decode('utf-8')
        try:
          data = json.loads(body)
          if data and headers:
            headers['headers'] = dict(headers)
          if data and data.get('errors'):
            return self._log_graphql_error(query, data)
          return data
        except json.JSONDecodeError as exc:
          return self._log_json_error(body, exc)
    except HTTPError as exc:
      return self._log_http_error(query, req, exc)
  
  # By default, this is a post request -- the API can be rewritten to accommodate a separate GET request
  def get_request(self, query, variables, operation_name, headers):
    post_data = json.dumps(
      {
        'query': query,
        'variables': variables,
        'operationName': operation_name
      }
    ).encode('utf-8')
    headers.update(
      {
        'Content-Type': 'application/json',
        'Content-Length': len(post_data)
      }
    )

    return urllib3.request(
      method=self.method, # POST
      url=self.url,
      body=post_data,
      headers=headers
    )

  def _log_json_error(self, body, exc):
    return {
      'data': None,
      'errors': [
        {
          'message': str(exc),
          'exception': exc,
          'body': body
        }
      ]
    }

  def _log_http_error(self, query, req, exc):
    self.logger.error('%s: %s', req.get_url(), exc)
    for h in sorted(exc.headers):
      self.logger.info('Response header: %s: %s', h, exc.headers[h])

    body = exc.read().decode('utf-8')
    content_type = exc.headers.get('Content-Type', '')
    self.logger.info('Response [%s]: \n%s', content_type, body)
    if not content_type.startswith('application/json'):
      return {
        'data': None,
        'errors': [
          {
            'message': str(exc),
            'exception': exc,
            'status': exc.code,
            'headers': exc.headers,
            'body': body
          }
        ]
      }
    else:
      try:
        data = json.loads(body)
      except json.JSONDecodeError as exc:
        return self._log_json_error(body, exc)
      
      if isinstance(data, dict) and data.get('errors'):
        data.update(
          {
            'exception': exc,
            'status': exc.code,
            'headers': exc.headers
          }
        )
        return self._log_graphql_error(query, data)
      return {
        'data': None,
        'errors': [
          {
            'message': str(exc),
            'exception': exc,
            'status': exc.code,
            'headers': exc.headers,
            'body': body
          }
        ]
      }
    
  def _fixup_graphql_error(self, data):
    original_data = data
    errors = data.get('errors')
    original_errors = errors
    if not isinstance(errors, list):
        self.logger.warning(
            'data["errors"] is not a list! Fix up data=%r', data
        )
        data = data.copy()
        data['errors'] = [{'message': str(errors)}]
        return data

    for i, error in enumerate(errors):
        if not isinstance(error, dict):
            self.logger.warning(
                'Error #%d: is not a dict: %r. Fix up!', i, error
            )
            if data is original_data:
                data = data.copy()
            if errors is original_errors:
                errors = errors.copy()
                data['errors'] = errors

            errors[i] = {'message': str(error)}
            continue

        message = error.get('message')
        if not isinstance(message, str):
            if data is original_data:
                data = data.copy()
            if errors is original_errors:
                errors = errors.copy()
                data['errors'] = errors

            message = str(error) if message is None else str(message)
            error = error.copy()
            error['message'] = message
            errors[i] = error

    return data
    
  def _log_graphql_error(self, query, data):
    if isinstance(query, bytes):
        query = query.decode('utf-8')
    elif not isinstance(query, str):
        query = bytes(query).decode('utf-8')

    data = self._fixup_graphql_error(data)
    errors = data['errors']
    self.logger.error('GraphQL query failed with %s errors', len(errors))
    for i, error in enumerate(errors):
        paths = error.get('path')
        if paths:
            paths = ' ' + '/'.join(str(path) for path in paths)
        else:
            paths = ''
        self.logger.info('Error #{}{}:'.format(i, paths))
        for ln in error.get('message', '').split('\n'):
            self.logger.info('   | {}'.format(ln))

        s = self.snippet(query, error.get('locations'))
        if s:
            self.logger.info('   -')
            self.logger.info('   | Locations:')
            for ln in s:
                self.logger.info('   | {}'.format(ln))
    return data