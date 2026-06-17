import pytest
from hardpycover.core.base import RequestCounter
from hardpycover.core.exceptions import RateLimitExceededError


def test_counter_increments():
  counter = RequestCounter(rate_limit=60)
  counter.check_and_increment()
  assert counter.current_count == 1


def test_counter_raises_at_limit():
  counter = RequestCounter(rate_limit=3)
  counter.check_and_increment()
  counter.check_and_increment()
  counter.check_and_increment()
  with pytest.raises(RateLimitExceededError):
    counter.check_and_increment()


def test_counter_resets_after_window(monkeypatch):
  start = 0.0
  monkeypatch.setattr("hardpycover.core.base.time.time", lambda: start)
  counter = RequestCounter(rate_limit=2)
  counter.check_and_increment()
  counter.check_and_increment()
  # Advance time past the 60-second window
  monkeypatch.setattr("hardpycover.core.base.time.time", lambda: start + 61.0)
  # Should not raise — window has reset
  counter.check_and_increment()
  assert counter.current_count == 1


def test_counter_rate_limit_property():
  counter = RequestCounter(rate_limit=60)
  assert counter.rate_limit == 60


def test_client_raises_rate_limit_error(valid_client, mocker):
  mock_response = mocker.MagicMock(return_value={
    "data": {"search": {"error": None, "page": 1, "per_page": 50,
                        "results": {"found": 0, "page": 1, "hits": []}}}
  })
  mocker.patch.object(valid_client.query, "_client", mock_response)
  # Exhaust the counter
  valid_client.query._request_counter._count = valid_client.query._request_counter._rate_limit
  with pytest.raises(RateLimitExceededError):
    valid_client.query.books("Dune")
