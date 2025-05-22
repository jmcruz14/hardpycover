from .core.base import GraphQLClient
from .core.const import endpoint_url
from .utils import clean_api_key
from typing import Dict, Any

class Hardcover:
  def __init__(self, api_key: str):
    headers = {
      'Content-Type': 'application/json',
      'Authorization': clean_api_key(api_key) # confirm if this is okay
    }
    self.client = GraphQLClient(endpoint_url, headers)

  def get_user(self, user_id: str = None) -> Dict[str, Any]:
    """Get user by ID"""

    query = """
      query GetUser {
        me {
          id
        }
      }
    """
    return self.client.execute(query)