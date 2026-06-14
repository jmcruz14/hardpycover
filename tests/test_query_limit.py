import pytest
import secrets
from sgqlc.operation import GraphQLErrors

# TODO: add test case for when query_limit_nonnegative

@pytest.fixture(scope="module")
def randomized_query_limit():
  random_num = secrets.choice(range(1,51))
  yield random_num

def test_query_limit_capped_to_fifty(valid_client, capsys):
  valid_client.query.books("Dune", limit=51)
  captured = capsys.readouterr()
  assert captured.out == "Query request exceeds limit, setting to limit...\n"

# NOTE: explore parameterizing this with various endpoints?
def test_query_limit_works(valid_client, randomized_query_limit):
  result = valid_client.query.publishers(limit=randomized_query_limit)
  publishers = result["publishers"]
  assert len(publishers) == randomized_query_limit, "Query limit does not match"

# def test_query_limit_is_nonnegative(valid_client):
#   with pytest.raises(GraphQLErrors, match="expected a non-negative 32-bit integer"):
#     books = valid_client.query.books("Dune", limit=-1)
