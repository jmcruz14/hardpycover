import time
import logging
from collections.abc import Callable
from sgqlc.endpoint.requests import RequestsEndpoint
from .exceptions import RateLimitExceededError

logger = logging.getLogger(__name__)

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

class RequestCounter:
  def __init__(self, rate_limit: int = 60):
    self._rate_limit = rate_limit
    self._count = 0
    self._window_start = time.time()

  def check_and_increment(self):
    now = time.time()
    if now - self._window_start >= 60:
      self._count = 0
      self._window_start = now
    if self._count >= self._rate_limit:
      raise RateLimitExceededError(self._rate_limit)
    self._count += 1

    if (self._rate_limit / 2) == self._count:
      logger.warning("At least 50% of rate limit has been exceeded")

  @property
  def current_count(self) -> int:
    return self._count

  @property
  def rate_limit(self) -> int:
    return self._rate_limit