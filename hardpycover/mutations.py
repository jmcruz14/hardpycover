from sgqlc.operation import Operation
from .schema import mutation_root as Mutation


class Mutations:
  def __init__(self, client, query_limit=50, request_counter=None):
    self._client = client
    self._query_limit = query_limit
    self._request_counter = request_counter

  def _run_mutation(self):
    return Operation(Mutation)

  def _check_rate_limit(self):
    if self._request_counter:
        self._request_counter.check_and_increment()

  # def update_user(
  #   self,
  #   user_id: int,
  #   **User
  # ):
  #   op = self._run_mutation()
  #   try:
  #     op.update_user()
  #   except GraphQLErrors as ex:
  #     print("GraphQLError: %s" % ex.errors)
  #     return None
  #   except Exception as e:
  #     print("Error: %s" % e)
  #     return None
