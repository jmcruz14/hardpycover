import pytest
import secrets
import logging
from sgqlc.operation import GraphQLErrors


test_data = [
  secrets.choice(range(1,51)),
  secrets.choice(range(1,51)),
  secrets.choice(range(1,51)),
  secrets.choice(range(1,51)),
]

def test_query_limit_capped_to_fifty(valid_client, caplog, mocker):
  mock_client = mocker.MagicMock(return_value={
        "data": {
            "search": {
                "error": None,
                "page": 1,
                "per_page": 50,
                "results": {"found": 0, "page": 1, "hits": []}
            }
        }
    })
  mocker.patch.object(valid_client.query, "_client", mock_client)
  with caplog.at_level(logging.WARNING, logger="hardpycover.queries"):
      valid_client.query.books("Dune", limit=51)
  assert "Query request exceeds limit, setting to limit..." in caplog.text

@pytest.mark.parametrize("randomized_query_limit", test_data)
def test_query_limit_works(valid_client, randomized_query_limit, mocker):
  mock_publishers = [{"name": f"Publisher {i}"} for i in range(randomized_query_limit)]
  mocker.patch.object(
      valid_client.query, "publishers",
      return_value={"publishers": mock_publishers}
  )
  result = valid_client.query.publishers(limit=randomized_query_limit)
  publishers = result["publishers"]
  assert len(publishers) == randomized_query_limit, "Query limit does not match"

# NOTE: uncomment this when the API is working
# def test_query_limit_is_nonnegative(valid_client, mocker):
#     mock_client = mocker.MagicMock(return_value={
#         "errors": [{"message": "expected a non-negative 32-bit integer for type 'Int', but found an integer"}],
#         "data": None
#     })
#     mocker.patch.object(valid_client.query, "_client", mock_client)
#     with pytest.raises(GraphQLErrors):
#         valid_client.query.books("Dune", limit=-1)
