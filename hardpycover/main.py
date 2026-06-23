import logging
from typing import Literal
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

logger = logging.getLogger(__name__)
class Hardcover(Client):
  """
    Orchestration class for consolidating the `Client` instance
    along with additional guardrails like rate limit, query limit,
    and the query+mutation factories part of the Hardcover API.

    Args:
      return_json (bool): flag for serving data as a JSON object or as a sgqlc_query object
  """

  def __init__(self, *args: Client, return_json: bool = True, **kwargs: Client):
    self._query_limit: int = 50  # Hardcoded limit
    self._rate_limit: int = 60 # currently 60/min
    super().__init__(*args, **kwargs)
    _counter = RequestCounter(self._rate_limit)
    self.query: Queries = Queries(self.client, return_json, self._query_limit, _counter)
    self.mutation: Mutations = Mutations(self.client, self._query_limit, _counter)
    # NOTE: explore inclusion of auto_validate config? depth fetching?

  @classmethod
  def get_resource_link(
    cls,
    resource_id: int,
    model_type: Literal["book", "series", "author", "character",
      "edition", "publisher", "user"] = "book",
    sub_path: str | dict | None = None
  ) -> str:
    """
      Returns a stable URL link that reliably links to a specific item.

      The method follows a guide from the `official docs <https://docs.hardcover.app/api/guides/linkingbyid/#supported-models>`__
      where a stable URL can be used to access a resource.

      Args:
        id (int): id value of resource
        model_type (Literal(str)): model type of resource (`book`, `series`, `author`, `character`,
          `edition`, `publisher`, `user` currently supported)
        sub_path (str or dict or None): sub-path to append to the link

      Returns:
        url (str): Hardcover URL
    """
    try:
      HARDCOVER_URL = "https://hardcover.app"
      stable_url = f"{HARDCOVER_URL}/id/{model_type}/{resource_id}"

      if sub_path and isinstance(sub_path, dict):
        if len(sub_path) > 1:
          raise ValueError("Sub-path of dict type must be of a single key-value pair only")

        # NOTE: is this fast?
        (_model, _value), = sub_path.items()
        stable_url = f"{stable_url}/{_model}/{_value}"

        # NOTE: no need to check if resource is valid... right?

      if sub_path and isinstance(sub_path, str):
        stable_url = f"{stable_url}/{sub_path}"

      return stable_url
    except ValueError as e:
      logger.error(f"ValueError: {e}")
    except Exception as e:
      logger.error(f"Error: {e}")

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