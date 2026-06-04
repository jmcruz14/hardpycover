from typing import Optional, List, Dict, Any
from sgqlc.operation import Operation, GraphQLErrors
from pydantic import ValidationError

from .classes import User, UserBook, UserBooksAggregate, Search, Publisher, Author, Me
from .filter import _get_critical_book_fields
from .schema import (
  user_books_select_column,
  editions_select_column,
  query_root as Query
)
from .stats import (
  _build_time_filter,
  _select_stat_fields,
  _flatten_result
)

class Queries:
  def __init__(self, client, query_limit: int = 50):
    self._client = client
    self._query_limit = query_limit
  
  def _run_op(self):
    return Operation(Query)

  def user_profile(
    self,
    fields: Optional[List[str]] = None
  ) -> dict:
    """Returns user profile.

    Args:
      fields (list(str)): List of acceptable fields based on `User` class in API.
    
    Returns:
      user (dict): User information
    """
    DEFAULT_USER_FIELDS = Me.model_fields.keys()

    op = self._run_op()
    try:
      me = op.me()
      if fields:
        me.__fields__(*fields)
      else:
        me.__fields__(*DEFAULT_USER_FIELDS)
      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      return raw
    except GraphQLErrors as ex:
      print("GraphQLError: %s" % ex.errors)
      return None
    except Exception as e:
      print("Error: %s" % e)
      return None
  
  def user_stats(
    self, 
    user_id: int,
    stats: list[str] = [], 
    start_date: str = None,
    end_date: str = None
  ):
    """
      Retrieve user stats based on user_id

      Args:
        user_id (int): hardcover user id
        stats (list(str)): selected key stats for querying
        start_date (str): datetime expressed as a string
        end_date (str): datetime expressed as a string
      
      Returns:

    """

    op = self._run_op()
    try:
      if not user_id:
        raise ValueError("Please input a User ID.")

      time_filter = _build_time_filter(start_date=start_date, end_date=end_date)
      where = {"user_id": {"_eq": user_id}, **time_filter}
      uba = op.user_books_aggregate(where=where)
      agg = uba.aggregate
      results = _select_stat_fields(stats)
      if len(results['aggregate']) > 0:
        for item in results.get('aggregate'):
          for agg_func, field in item.items():
            getattr(agg, agg_func).__fields__(*field)
        
      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      return raw

      # NOTE: flattening results temporarily on hold
      # data = raw["data"]
      # res = _flatten_result(data)
      # return res

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
    offset: int = 0
  ) -> Dict[str, Any]:
    """
      Get owned books based on user_id

      Args:
        user_id (int): associated user_id
        limit (int): query limit, max = 50, default = 25
        offset (int): query offset, default = 0

      Returns:
        owned_books (list(dict)): list of owned books
    """
    if limit > self._query_limit:
      print("Query request exceeds limit, setting to limit...")
      limit = 50

    op = self._run_op()
    try:
      # user_books = op.user_books(where={'slug': {'_eq': 'owned'}}, limit=limit, distinct_on=[user_books_select_column.book_id], offset=offset)
      user_books = op.user_books(where={'user_id': {'_eq': user_id}}, limit=limit, distinct_on=[user_books_select_column.book_id], offset=offset)
      user_books.__fields__("id", "user_id", "created_at")
      user_books.book.__fields__("id","title", "subtitle", "rating", "release_year")
      user_books.edition.__fields__("isbn_10", "isbn_13", "edition_format", "edition_information")
      user_books.edition.language.__fields__("code2", "language")

      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      return raw

      # ub = raw["data"]["user_books"]
      # for book in ub:
      #   UserBook.model_validate(book)
      # return ub
    
    except Exception as e:
      print("Error found %s" % e)
  
  # Supports name search and generic author search
  # NOTE: planned updates - flag to include author's books, id search
  def authors(
    self, 
    author_name: Optional[str] = None,
    author_id: Optional[int] = None, # NOTE: implement patch for id search
    limit: int = 10,
    offset: int = 0
  ):
    if limit > self._query_limit:
      print("Query request exceeds limit, setting to limit...")
      limit = 50

    where = {
      "state": {"_neq": "duplicate"}
    }
    
    if author_name:
      where["name"] = {"_eq": author_name}
      
    arguments = {
      "where": {**where},
      "limit": limit,
    }

    if offset:
      arguments["offset"] = offset

    op = self._run_op()
    try:
      authors = op.authors(where=arguments)
      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      return raw
    
      # if result is False:
      #   raise ValueError
      # authors = result["data"]
      # if not authors:
      #   raise ValueError

      # for a in authors["authors"]:
      #   Author.model_validate(a)
      # return authors
    except ValidationError as e:
      print(e)
      return None
    except ValueError as e:
      print(e)
      return None
  
  def books(
    self, 
    search: str, 
    limit: int = 25,
    offset: int = 0,
    # include_contribtions: bool = False
    detailed = False
  ):
    """Search books from database.

    Args:
      search (str): Query string to be used for search.
      limit (int): Number of results
      skip: (int): Skip n results

    Returns:
      books (dict): List of books
    """
    if limit > self._query_limit:
      print("Query request exceeds limit, setting to limit...")
      limit = 50

    # NOTE: include possible update for more customizable search params
    arguments = {
      "query": search,
      "query_type": "book",
      "per_page": limit
    }
    if offset:
      arguments["offset"] = offset

    op = self._run_op()
    try:
      search = op.search(**arguments)
      search.__fields__("error", "page", "per_page", "results")
      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      return raw
    except ValidationError as e:
      print(e)
    except ValueError as e:
      print(e)
  
  def book_characters(
    self,
    book_id: Optional[int] = None,
    limit: int = 25
  ):
    where = {
      "book_id": {"_eq": book_id}
    }
    
    op = self._run_op()
    try:
      bc = op.book_characters(where=where, limit=limit)
      bc.__fields__("id", "character_id", "only_mentioned", "position", "spoiler")
      bc.character.__fields__("name", "is_lgbtq", "has_disability", "gender_id", "books_count", "biography")
      bc.book.__fields__("title", "id")
      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      return raw
    
    except ValidationError as e:
      print(e)
    except ValueError as e:
      print(e)

  def user_books_progress(
    self,
    limit: int = 25
  ):
    if limit > self._query_limit:
      print("Query request exceeds limit, setting to limit...")
      limit = 50

    op = Operation(Query)
    try:
      where = {"where": {"status_id": {"_eq": 2}}}
      me = op.me()
      ub = me.user_books(where=where)
      ub.__fields__("id")
      ub.user_book_reads.__fields__("progress", "progress_pages")
      ub.book.__fields__("id", "title", "pages")
      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      return raw
    except ValidationError as e:
      print(e)
    except ValueError as e:
      print(e)

  def book_editions(
    self,
    title: str,
    limit: int = 25
  ):
    """
      Fetches all editions of a book.

      Args:
        title (str): book title
      
      Returns:
        result (dict):
    """
    if limit > self._query_limit:
      print("Query request exceeds limit, setting to limit...")
      limit = 50

    op = Operation(Query)
    where = {"title": {"_eq": title}, "state": {"_eq": "normalized"}}
    try:
      editions = op.editions(where=where, limit=limit)
      editions.__fields__("id", "title", "edition_format", "pages", "release_date", "isbn_10", "isbn_13")
      editions.publisher.__fields__("name")
      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      return raw
    except ValidationError as e:
      print(e)
    except ValueError as e:
      print(e)

  def publishers(
    self,
    publisher_name: str = None, 
    limit: int = 25, 
    offset: int = 0
  ):
    if limit > self._query_limit:
      print("Query request exceeds limit, setting to limit...")
      limit = 50

    where = {
      "state": {"_neq": "duplicate"}
    }
    if publisher_name:
      where["name"] = {"_eq": publisher_name}

    arguments = {
      "where": {**where},
      "limit": limit,
    }
    if offset:
      arguments["offset"] = offset
    
    op = Operation(Query)
    publisher_fields = Publisher.model_fields.keys()
    try:
      op.publishers(where=where)
      op.publishers.__fields__(*publisher_fields)
      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      return raw
      # result = raw["data"]
      # publishers = result["publishers"]
      # if not publishers:
      #   raise ValueError("No publishers data found.")
      
      # # Run validation
      # for i, p in enumerate(publishers):
      #   p = Publisher(**p)
      #   p = p.model_dump(mode="json", exclude_none=True)
      #   publishers[i] = p

      # return publishers
    except ValidationError as e:
      print(e)
      return None
    except ValueError as e:
      print(e)
      return None