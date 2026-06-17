import pytest
from hardpycover.classes import Me

@pytest.fixture
def me_result(valid_client, mocker):
  mock_data = {
    "me": [
      {
        "access_level": 1,
        "account_privacy_setting_id": 1,
        "activity_privacy_settings_id": 1,
        "timezone": "Asia/Manila",
        "username": "bob",
        "object_type": "User",
      }
    ]
  }
  # NOTE: this mocks the user_profile() method in the valid_client.query subclass
  mocker.patch.object(valid_client.query, "user_profile", return_value=mock_data)
  result = valid_client.query.user_profile()
  yield result["me"]

def test_me_is_one_length_array(me_result):
  me = me_result
  assert len(me) == 1

def test_me_is_user_object(me_result):
  me = me_result[0]
  assert Me.model_validate(me)
  assert me["object_type"] == "User", "me object is not of object_type `User`"