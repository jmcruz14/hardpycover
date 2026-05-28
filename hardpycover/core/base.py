import json
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from typing import Dict, Optional
from .exceptions import GraphQLError

__all__ = ('GraphQLClient')

class GraphQLClient:
  """
  Instantiate a standard GraphQL client.

  Args:
    endpoint (str): The API endpoint to be used for the request
    headers (dict): Headers to be passed alongside request
  """

  def __init__(
    self, 
    endpoint: str, 
    headers: Optional[Dict[str, str]] = None
  ):
    self.endpoint = endpoint
    self.headers = headers or {}

    if 'Content-Type' not in self.headers:
      self.headers['Content-Type'] = 'application/json'

  def execute(self, query: str):
    payload = {
      'query': query
    }

    data = json.dumps(payload).encode('utf-8')

    try:
      request = urllib.request.Request(
        self.endpoint,
        data=data,
        headers=self.headers,
        method='POST'
      )
    
      with urlopen(request) as response:
        response_data = json.loads(response.read().decode('utf-8'))
      if 'errors' in response_data:
        raise GraphQLError(
          errors=response_data['errors'],
          data=response_data.get('data')
        )
      
      return response_data.get('data', {}) # default
    
    except HTTPError as e:
      # Return custom exception based on HTTP error code
      code = e.code
      # body = e.read().decode('utf-8') if e.fp else 'No error details'
      if code == 401:
        print(f"HTTP {code}: Bearer token invalid/expired.")
        return False
      if code == 403:
        print(f"HTTP {code}: User does not have access to requested resource.")
        return False
      
      # raise HTTPError(
      #   e.url, e.code, f"HTTP {e.code}: {error_body}", e.headers, e.fp
      # )
    
    # TODO: implement cleaner exception handling
  
  def set_auth_token(self, token: str, token_type: str = 'Bearer'):
    """
    Set authentication token.

    Args:
      token: The authentication token
      token_type: The token type (e.g, 'Bearer', 'Token')
    """

    if 'Bearer' in token:
      self.headers['Authorization'] = f'{token}'
    elif 'Bearer' not in token and token_type == 'Bearer':
      token = token.replace(' ', '')
      self.headers['Authorization'] = f'Bearer {token}'

### build test cases somewhere?