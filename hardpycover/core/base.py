import json
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from typing import Dict, Optional
from .exceptions import GraphQLError

from sgqlc.endpoint.requests import RequestsEndpoint

# NOTE: sgqlc rewrite requires incorporating types and operations
# expected time: 1-2 days if sole focus
# TODO: engineering decision: how to write in mutation calls and
class Client:
  def __init__(
    self,
    token,
    url = "https://api.hardcover.app/v1/graphql",
  ):
    header = {
      "authorization": ("Bearer %s" % token)
    }
    self.client = RequestsEndpoint(url, base_headers=header, timeout=30)
  
  def __str__(self):
    return str(self.client)

  def __call__(self, *args, **kwargs):
    return self.client(*args, **kwargs)
  
  def _get_request(self, *args, **kwargs):
    return self.client(method="GET", *args, **kwargs)

  def _post_request(self, *args, **kwargs):
    return self.client(method="POST", *args, **kwargs)