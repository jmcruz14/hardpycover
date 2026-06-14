import pytest
import os
from hardpycover import Hardcover

REAL_TOKEN = os.getenv('BEARER_TOKEN')
FALSE_TOKEN = "false_invalid_token_xyz"

@pytest.fixture(scope="session")
def valid_client():
    return Hardcover(REAL_TOKEN)

@pytest.fixture # Default scope: function
def invalid_client():
    return Hardcover(FALSE_TOKEN)
