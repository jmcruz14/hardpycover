from .core.base import GraphQLClient
from .core.http import endpoint_url
from .core.query import create_query
from .classes import User, UserBook, Search
from .utils import clean_api_key
from .filter import get_critical_book_fields

from typing import Dict, Any, List, Optional
from pydantic import ValidationError

from pprint import pprint

class Hardcover:
  def __init__(self, api_key: str):
    headers = {
      'Content-Type': 'application/json',
      'Authorization': clean_api_key(api_key) # confirm if this is okay
    }
    self.client = GraphQLClient(endpoint_url, headers)

  def get_user(self, fields: Optional[List[str]] = None) -> Dict[str, Any]:
    """Get your user information.
    
    Args:
      fields (list(str)): List of acceptable fields based on the User class"""
    
    try:
      table_name = "me"
      query = create_query(User, table_name, selected_fields=fields)

      # validation layer
      result = self.client.execute(query)

      if result is False:
        raise ValueError

      output = result[table_name][0]

      # Validate before serialization
      User.model_validate(output)
      u = User(**output)
      return u.model_dump(by_alias=True)
    
    except ValidationError as e:
      print(e)
    except ValueError as e:
      print(e)
  
  # NOTE: rewrite query process for further customization
  def get_owned_books(
      self, 
      user_id: int, 
      fields: Optional[List[str]] = None,
      limit: int = 10
    ) -> Dict[str, Any]:
    """
      Get owned books based on user_id

      Args:
        user_id (int): associated user_id

    """
    table_name = "user_books"
    query = create_query(
      UserBook, 
      table_name, 
      selected_fields=fields,
      arguments = {
        'where': {
          'user_id': { '_eq': user_id}
        },
        'limit': limit
      }
    )

    result = self.client.execute(query)
    output = result[table_name][0]

    try:
      UserBook.model_validate(output)
      return output
    except ValidationError as e:
      print(e)
  
  # TODO: prioritize this
  def search_authors(self, search: str):
    # most popular? sort by? owned
    pass

  def search_books(self, search: str, per_page: int = 25, detailed = False):
    """Search books from database.

    Args:
      query (str): Query string to be used for search.

    Returns:
      books (dict): List of books
    """

    try:
      table_name = "search"
      query = create_query(Search, table_name, arguments={
        "query": search,
        "per_page": per_page
      })

      result = self.client.execute(query)
      if result is False:
        raise ValueError
      
      # Trim search result query

      if detailed:
        # NOTE: detailed output should be untrimmed json output
        pass

      result = result["search"]["results"]["hits"]
      if len(result) > 0:
        result = list(map(get_critical_book_fields, result))
        return result
      
      return None
    except ValidationError as e:
      print(e)
    except ValueError as e:
      print(e)
    
  def get_reading_list(self):
    pass

  def get_book_recommendation(self):
    pass

  
  # next question: how to incorporate the functionalities of all
  # available functions?
