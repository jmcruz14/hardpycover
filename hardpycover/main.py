from .core import Client
from .queries import Queries
from .mutations import Mutations

# TODO: standardize exception handling

# NOTE: we declare hardcover as a subclass of Client
# instead of directly calling the client
# so that the package is highly modular

# NOTE: Hardcover is declared as an orchestrator to ensure
# future queries can be coupled properly
# Hardcover(BEARER_TOKEN)
class Hardcover(Client):
	def __init__(self, *args, return_json: bool = True, **kwargs):
		self._query_limit = 50  # Hardcoded limit
		super().__init__(*args, **kwargs)
		self.query = Queries(self.client, return_json, self._query_limit)
		self.mutation = Mutations(self.client, self._query_limit)
		# NOTE: explore inclusion of auto_validate config? depth fetching?

	@property
	def query_limit(self):
		return self._query_limit


# NOTE: read https://typesense.org/ as this is the basis for logic (optimized search)
# NOTE: explore the implementation of the other method for accessing the hardcover endpoint -> via http.py -> urllib3