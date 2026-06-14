import pytest
from hardpycover.classes import Me

@pytest.fixture(scope="module")
def me_result(valid_client):
  result = valid_client.query.user_profile()
  me = result["me"]
  yield me

def test_me_is_one_length_array(me_result):
  me = me_result
  assert len(me) == 1

def test_me_is_user_object(me_result):
  me = me_result[0]
  assert Me.model_validate(me)
  assert me["object_type"] == "User", "me object is not of object_type `User`"