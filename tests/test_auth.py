from tests.conftest import REAL_TOKEN

# (a) instance created with working API key
def test_valid_api_key_sets_auth_header(valid_client):
    """Verify that a mock API key is stored and the Authorization header is correctly set."""
    headers = valid_client.client.base_headers
    assert "authorization" in headers
    assert headers["authorization"] == f"Bearer {REAL_TOKEN}"


# (b) instance created with false API key
def test_false_api_key_query_returns_none(invalid_client, mocker):
    """Verify that a false API key results in an auth error and the query returns None."""
    mock_call = mocker.MagicMock()
    mock_call.return_value = {
        "errors": [{"message": "Invalid authorization token"}],
        "data": None,
    }
    invalid_client.query._client = mock_call
    result = invalid_client.query.user_profile()
    assert result is None