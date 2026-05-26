from .core import GraphQLClient
from .core.http import endpoint_url
from .core.query import create_query
from .classes import User, UserBook, UserBooksAggregate, Search, Publisher, Author
from .utils import _clean_api_key
from .filter import _get_critical_book_fields


from .stats import _build_time_filter, _select_stat_fields, _flatten_result

from pydantic import ValidationError

QUERY_LIMIT = 50 # Hardcoded limit

# TODO: standardize exception handling

class Hardcover:
  def __init__(self, api_key: str):
    headers = {
      'Content-Type': 'application/json',
      'Authorization': _clean_api_key(api_key)
    }
    self.client = GraphQLClient(endpoint_url, headers)

  def user_profile(self, fields: Optional[List[str]] = None) -> Dict[str, Any]:
    """Get your user information.
    
    Args:
      fields (list(str)): List of acceptable fields based on the User class
    
    Returns:
      user (dict): User information
    """
    
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

  def user_stats(
      self, 
      user_id: int,
      stats: list[str] = [], 
      start_date: str = None,
      end_date: str = None
    ) -> Dict[str, Any]:
    """
      Retrieve user stats based on user_id

      Args:
        user_id (int): user_id of selected user
        stats (list[str]): "listed"
    """
    
    table_name = "user_books_aggregate"
    try:
      time_filter = _build_time_filter(start_date=start_date, end_date=end_date)
      selected_fields = _select_stat_fields(stats)

      query = create_query(
        UserBooksAggregate,
        table_name,
        "UserStats",
        selected_fields=selected_fields,
        arguments={
          "where": {"user_id": {"_eq": user_id}, **time_filter}
        }
      )
      result = self.client.execute(query)
      result = _flatten_result(result)
      return result
    
    except ValidationError as e:
        print(e)
        return None
    except ValueError as e:
        print(e)
        return None


  def owned_books(
      self, 
      user_id: int,
      limit: int = 25,
      page: int = 1
      # NOTE: add field for status
    ) -> Dict[str, Any]:
    """
      Get owned books based on user_id

      Args:
        user_id (int): associated user_id

      Returns:
        owned_books (list(dict)): list of owned books
    """
    table_name = "user_books"
    selected_fields = [
      "id",
      "user_id",
      "created_at",
      {
        "book": ["id", "title", "subtitle", "rating", "release_year"]
      },
      {
        "edition": [
          "isbn_10", 
          "isbn_13",
          "edition_format", 
          "edition_information",
          {
            "language": ["code2", "language"]
          }
        ]
      }
    ]
    arguments = {
        'where': {
          'user_id': { '_eq': user_id},
          # 'owned': { '_eq': 'true' } # NOTE: using this condition does not return anything if testing with my account
          'user_book_status': { 'status': {'_neq': 'Want to Read'}}
        },
        'limit': limit,
      }
    
    # NOTE: maybe combine want to read and owned = true?
    # NOTE: include book edition
    
    if page > 1:
      arguments["offset"] = page * limit

    query = create_query(
      UserBook, 
      table_name, 
      selected_fields=selected_fields,
      arguments=arguments
    )

    result = self.client.execute(query)
    output = result[table_name]
    try:
      for book in output:
        UserBook.model_validate(book)
    except ValidationError as e:
      print(e)
  
    return output
  
  def authors(
    self, 
    author_name: str,
    per_page: int = 10,
    skip: int = 0
  ):
    if per_page > QUERY_LIMIT:
      print("Query request exceeds limit, setting to limit...")
      per_page = 50
    conditionals = {
      "state": {"_neq": "duplicate"}
    }
    if author_name:
      conditionals["name"] = {"_eq": author_name}

    arguments = {
      "where": {**conditionals},
      "limit": per_page,
    }
    if skip:
      arguments["offset"] = skip

    try:
      table_name = "authors"
      query = create_query(Author, table_name, arguments=arguments)
      result = self.client.execute(query)
      
      if result is False:
        raise ValueError

      return result["authors"]
    except ValidationError as e:
      print(e)
      return None
    except ValueError as e:
      print(e)
      return None

  def books(
    self, 
    search: str, 
    per_page: int = 25,
    skip: int = 0,
    # include_contribtions: bool = False
    detailed = False
  ):
    """Search books from database.

    Args:
      query (str): Query string to be used for search.

    Returns:
      books (dict): List of books
    """

    if per_page > QUERY_LIMIT:
      print("Query request exceeds limit, setting to limit...")
      per_page = 50

    arguments = {
      "query": search,
      "per_page": per_page
    }
    if skip:
      arguments["offset"] = skip

    try:
      table_name = "search"
      query = create_query(Search, table_name, arguments=arguments)
      result = self.client.execute(query)
      if result is False:
        raise ValueError
      
      # Trim search result query

      # if include_contributions:

      if detailed:
        # NOTE: detailed output should be untrimmed json output
        pass

      result = result["search"]["results"]["hits"]
      if len(result) > 0:
        result = list(map(_get_critical_book_fields, result))
        return result
      
      return None
    except ValidationError as e:
      print(e)
    except ValueError as e:
      print(e)
  
  def publishers(self, publisher_name: str = None, per_page: int = 25, page: int = 0):
    table_name = "publishers" 
    if per_page > QUERY_LIMIT:
      print("Query request exceeds limit, setting to limit...")
      per_page = 50

    conditionals = {
      "state": {"_neq": "duplicate"}
    }
    if publisher_name:
      conditionals["name"] = { "_eq": publisher_name}

    arguments = {
      "limit": per_page,
      "where": {**conditionals}
    }
    if page:
      arguments["offset"] = page

    query = create_query(Publisher, table_name, arguments=arguments)

    result = self.client.execute(query)
    return result

  # NOTE: potentially useful api functions below
  def get_reading_list(self):
    pass

  def get_book_recommendation(self):
    pass

  
  # next question: how to incorporate the functionalities of all
  # available functions?

# NOTE: read https://typesense.org/ as this is the basis for logic (optimized search)
# 