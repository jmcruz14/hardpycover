from collections.abc import Callable
from sgqlc.endpoint.requests import RequestsEndpoint

# NOTE: sgqlc rewrite requires incorporating types and operations
# expected time: 1-2 days if sole focus
# TODO: engineering decision: how to write in mutation calls and
class Client:
  def __init__(
    self,
    token: str,
    url="https://api.hardcover.app/v1/graphql",
  ):
    header = {"authorization": ("Bearer %s" % token)}
    self._url: str = url
    self._token: str = token
    self.client: Callable = RequestsEndpoint(url, base_headers=header, timeout=30)

  # def __str__(self):
  #   return str(self.client)

  def __call__(self, *args, **kwargs) -> RequestsEndpoint:
    return self.client(*args, **kwargs)

  def get_request(self, *args, **kwargs) -> RequestsEndpoint:
    return self.client(method="GET", *args, **kwargs)

  def post_request(self, *args, **kwargs) -> RequestsEndpoint:
    return self.client(method="POST", *args, **kwargs)
