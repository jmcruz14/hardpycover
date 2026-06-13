import json
from typing import Dict, Any, Literal
from sgqlc.operation import Operation, GraphQLErrors
from pydantic import ValidationError

from .classes import (
  Author,
  Book,
  BookCharacter,
  Me,
  ReadingJournal,
  User,
  UserBook,
  UserBookReads,
  UserBooksAggregate,
  Edition,
  Series,
  Search,
  Publisher,
  )
from .filter import _get_critical_book_fields
from .schema import (
  user_books_select_column,
  editions_select_column,
  reading_journals_order_by,
  order_by as ORDER_BY,
  query_root as Query
)
from .stats import (
  _build_time_filter,
  _select_stat_fields,
  # _flatten_result
)

# NOTE: explore further orchestration
# from queries.authors import Authors as AQ (or just stop to prevent overutilization)

class Queries:
  def __init__(self, client, return_json, query_limit: int = 50):
    self._client = client
    self._return_json = return_json
    self._query_limit = query_limit

  def _run_op(self):
    return Operation(Query)

  def user_profile(
    self,
    fields: list[str] | None = None
  ) -> dict | None:
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
      res = op + raw
      r = res.me

      for u in r:
        Me.model_validate(u.__to_json_value__())

      if self._return_json:
        json = res.__to_json_value__()
        return json
      else:
        return res
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

      res = op + raw

      UserBooksAggregate.model_validate(res.user_books_aggregate.__to_json_value__(), strict=True)
      if self._return_json:
        json = res.__to_json_value__()
        return json
      else:
        return res
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
      res = op + raw

      ub = res.user_books
      for i in ub:
        UserBook.model_validate(i.__to_json_value__(), strict=True)

      if self._return_json:
        json = res.__to_json_value__()
        return json
      else:
        return res
    except Exception as e:
      print("Error found %s" % e)

  def authors(
    self,
    search: str,
    limit: int = 10,
    offset: int = 0
  ):
    """Search authors from database.

    Args:
      search (str): Query string to be used for search.
      limit (int): Number of results.
      offset (int): Skip n results.

    Returns:
      hits (list): List of matching authors.
    """
    if limit > self._query_limit:
      print("Query request exceeds limit, setting to limit...")
      limit = 50

    arguments = {
      "query": search,
      "query_type": "author",
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
      res = op + raw

      re = res.search.results
      hits = re['hits']

      for doc in hits:
        Author.model_validate(doc['document'])

      if self._return_json:
        json = hits.__to_json_value__()
        return json
      else:
        return hits
    except ValidationError as e:
      print(e)
    except ValueError as e:
      print(e)

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
      res = op + raw

      re = res.search.results
      found = re['found']
      page = re['page']
      hits = re['hits']
      # NOTE:

      # NOTE: if hits none -> put use case

      for doc in hits:
        Book.model_validate(doc['document'])

      return hits
    except ValidationError as e:
      print(e)
    except ValueError as e:
      print(e)

  def book_characters(
    self,
    book_id: int | None = None,
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
      res = op + raw

      bc = res.book_characters
      for i in bc:
        BookCharacter.model_validate(i.__to_json_value__(), strict=False)

      if self._return_json:
        json = res.__to_json_value__()
        return json
      else:
        return res

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
      res = op + raw
      m = res.me

      # NOTE: the validation layer for this one is off right now
      # TODO: update model validation for this in future update
      for i in m:
        Edition.model_validate(i.__to_json_value__())

      if self._return_json:
        json = m.__to_json_value__()
        return json
      else:
        return m
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
      res = op + raw

      for i in res.editions:
        Edition.model_validate(i.__to_json_value__())

      if self._return_json:
        json = res.editions.__to_json_value__()
        return json
      else:
        return res
    except ValidationError as e:
      print(e)
    except ValueError as e:
      print(e)

  def publishers(
    self,
    publisher_name: str | None = None,
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

    op = self._run_op()
    publisher_fields = Publisher.model_fields.keys()
    try:
      op.publishers(where=where)
      op.publishers.__fields__(*publisher_fields)
      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      res = op + raw

      for i in res.publishers:
        Publisher.model_validate(i.__to_json_value__())

      if self._return_json:
        json = res.__to_json_value__()
        return json
      else:
        return res
    except ValidationError as e:
      print(e)
      return None
    except ValueError as e:
      print(e)
      return None

  def reading_journals(
    self,
    user_id: int,
    limit: int = 10,
    offset: int = 0,
    sort: Literal["asc", "desc"] = "desc",
  ):
    if limit > self._query_limit:
      print("Query request exceeds limit, setting to limit...")
      limit = 50

    where = {"user_id": {"_eq": user_id}}
    order_by = reading_journals_order_by({"action_at": ORDER_BY(sort)})
    arguments = {
      "where": {**where},
      "limit": limit,
      "offset": offset,
      "order_by": [order_by] # NOTE: order_by argument is expected as a list_of
    }

    op = self._run_op()
    reading_journal_fields = ReadingJournal.model_fields.keys()
    try:
      rj = op.reading_journals(**arguments)
      rj.__fields__(*reading_journal_fields)
      rj.book.__fields__("title", "release_year")
      rj.edition.__fields__("publisher_id", "pages", "edition_format")
      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      res = op + raw

      # NOTE: implement data validation
      for i in res.reading_journals:
        ReadingJournal.model_validate(i.__to_json_value__())

      if self._return_json:
        json = res.__to_json_value__()
        return json
      else:
        return res
    except ValidationError as e:
      print(e)
      return None
    except ValueError as e:
      print(e)
      return None

  def series(
    self,
    search: str,
    limit: int = 10,
    offset: int = 0
  ):
    """Search authors from database.

    Args:
      search (str): Query string to be used for search.
      limit (int): Number of results.
      offset (int): Skip n results.

    Returns:
      hits (list): List of matching authors.
    """
    if limit > self._query_limit:
      print("Query request exceeds limit, setting to limit...")
      limit = 50

    arguments = {
      "query": search,
      "query_type": "series",
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
      res = op + raw

      re = res.search.results
      hits = re['hits']

      for doc in hits:
        Series.model_validate(doc['document'])

      if self._return_json:
        json = res.__to_json_value__()
        return json
      else:
        return hits
    except ValidationError as e:
      print(e)
    except ValueError as e:
      print(e)