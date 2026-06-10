from .classes import User
from sgqlc.operation import Operation, GraphQLErrors
from .schema import (
  mutation_root as Mutation
)

class Mutations:
  def __init__(self, client, query_limit = 50):
    self._client = client
    self._query_limit = query_limit

  def _run_mutation(self):
    return Operation(Mutation)
  
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