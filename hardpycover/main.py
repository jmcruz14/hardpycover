import logging
from .core import Client, RequestCounter
from .queries import Queries
from .mutations import Mutations

# TODO: standardize exception handling

# NOTE: we declare hardcover as a subclass of Client
# instead of directly calling the client
# so that the package is highly modular

# NOTE: debate on whether data should be flattened or returned as is?

# NOTE: Hardcover is declared as an orchestrator to ensure
# future queries can be coupled properly
# Hardcover(BEARER_TOKEN)

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s [%(levelname)s] %(message)s"
)

class Hardcover(Client):
  def __init__(self, *args: Client, return_json: bool = True, **kwargs: Client):
    self._query_limit: int = 50  # Hardcoded limit
    self._rate_limit: int = 60 # currently 60/min
    super().__init__(*args, **kwargs)
    _counter = RequestCounter(self._rate_limit)
    self.query: Queries = Queries(self.client, return_json, self._query_limit, _counter)
    self.mutation: Mutations = Mutations(self.client, self._query_limit, _counter)
    # NOTE: explore inclusion of auto_validate config? depth fetching?

  @property
  def query_limit(self):
    return self._query_limit

  @property
  def rate_limit(self):
      return self._rate_limit

  def __str__(self):
    return "%s(token=%s,url=%s,query_limit=%s)" % (
      self.__class__.__name__,
      self._token,
      self._url,
      self._query_limit
    )

  def __repr__(self):
    return self.__str__()

# NOTE: read https://typesense.org/ as this is the basis for logic (optimized search)
# NOTE: explore the implementation of the other method for accessing the hardcover endpoint -> via http.py -> urllib3