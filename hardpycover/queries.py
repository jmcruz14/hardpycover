import logging
from typing import Dict, Any, Literal, get_type_hints
from sgqlc.operation import Operation, GraphQLErrors
from pydantic import ValidationError

from .classes import (
  Activities,
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
  Platform,
  TrendingBooks,
  Publisher,
  PrivacySetting
  )
from .schema import (
  user_books_select_column,
  user_books_order_by,
  TrendingDuration,
  platforms_order_by,
  reading_journals_order_by,
  order_by as ORDER_BY,
  query_root as Query
)
from .stats import (
  build_time_filter,
  select_stat_fields,
  # flatten_result
)

# NOTE: explore further orchestration
# from queries.authors import Authors as AQ (or just stop to prevent overutilization)

logger = logging.getLogger(__name__)

class Queries:
  def __init__(self, client, return_json, query_limit: int = 50, request_counter = None):
    self._client = client
    self._return_json = return_json
    self._query_limit = query_limit
    self._request_counter = request_counter

  def _run_op(self):
    return Operation(Query)

  def _check_rate_limit(self):
    if self._request_counter:
        self._request_counter.check_and_increment()

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

    self._check_rate_limit()
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
      logger.error("GraphQLError: %s" % ex.errors)
    except Exception as e:
      logger.error("Error: %s" % e)

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

    self._check_rate_limit()
    op = self._run_op()
    try:
      if not user_id:
        raise ValueError("Please input a User ID.")

      time_filter = build_time_filter(start_date=start_date, end_date=end_date)
      where = {"user_id": {"_eq": user_id}, **time_filter}
      uba = op.user_books_aggregate(where=where)
      agg = uba.aggregate
      results = select_stat_fields(stats)
      if not results['aggregate']:
        raise ValueError("Empty aggregate results")

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
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)

  def user_reviews(
    self,
    user_id: int,
    limit: int = 25,
    offset: int = 0,
    sort: Literal["asc", "desc"] = "desc",
  ) :
    """
      Fetch user reviews based on user_id
    """
    if limit > self._query_limit:
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    self._check_rate_limit()
    op = self._run_op()
    try:
      where = {"user_id": {"_eq": user_id}, "has_review": {"_eq": True}}
      arguments = {
        "where": {**where},
        "order_by": [user_books_order_by({"reviewed_at": ORDER_BY(sort)})],
        "offset": offset,
        "limit": limit
      }
      ub = op.user_books(**arguments)
      ub.__fields__("id", "rating", "review", "review_has_spoilers", "reviewed_at")
      ub.book.__fields__("title")
      ub.book.image.__fields__("url")
      raw = self._client(op)
      res = op + raw

      books = res.user_books
      for book in books:
        UserBook.model_validate(book.__to_json_value__())

      if self._return_json:
        json = res.__to_json_value__()
        return json

      return res
    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)

  def user_activities(
    self,
    user_id: int,
    limit: int = 25,
    offset: int = 0
  ):
    if limit > self._query_limit:
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    # NOTE: not excluding privacy_setting makes the query too long
    fields = (x for x in Activities.model_fields.keys() if x != "privacy_setting")
    privacy_setting_fields = get_type_hints(PrivacySetting).keys()

    self._check_rate_limit()
    op = self._run_op()
    try:
      where = {"user_id": {"_eq": user_id}}
      arguments = {
        "where": {**where},
        "limit": limit,
        "offset": offset
      }
      activities = op.activities(**arguments)
      activities.__fields__(*fields)
      activities.privacy_setting.__fields__(*privacy_setting_fields)
      raw = self._client(op)
      res = op + raw

      activities = res.activities
      for a in activities:
        Activities.model_validate(a.__to_json_value__())

      if self._return_json:
        json = res.__to_json_value__()
        return json

      return res
    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
      return None
    except ValueError as e:
      logger.error("ValueError: %s" % e)
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
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    self._check_rate_limit()
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
      logger.error("Error found %s" % e)

  def book_characters(
    self,
    book_id: int | None = None,
    limit: int = 25
  ):
    if limit > self._query_limit:
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    where = {
      "book_id": {"_eq": book_id}
    }

    self._check_rate_limit()
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
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)

  def book_by_id(
    self,
    book_id: int
  ):
    where = {"id": {"_eq": book_id}}
    arguments = {
      "where": {**where},
      "limit": 1
    }

    self._check_rate_limit()
    op = self._run_op()
    try:
      book = op.books(**arguments)
      book.__fields__("id", "title")
      raw = self._client(op)
      res = op + raw

      return res
    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)\

  # TODO: create method for list activity, prompt activity, goal activity
  def book_activity(
    self,
    book_id: int,
    limit: int = 10,
    offset: int = 0
  ):
    if limit > self._query_limit:
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    where = {"book_id": {"_eq": book_id}, "event": {"_eq": "UserBookActivity"}}
    arguments = {
      "where": {**where},
      "limit": limit,
      "offset": offset
    }

    self._check_rate_limit()
    op = self._run_op()
    try:
      book_activity = op.activities(**arguments)
      book_activity.__fields__("book_id", "data", "event", "likes_count")
      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      res = op + raw

      return res
    except GraphQLErrors as ex:
      logger.error("GraphQLError: %s" % ex.errors)
    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)

  def trending_books(
    self,
    duration: Literal["all", "month", "one_year", "three_month", "week"] = "all",
    limit: int = 20,
  ):
    if limit > self._query_limit:
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    if duration not in duration:
      raise ValueError("Duration %s is not declared in accepted values" % duration)

    arguments = {
      "duration": TrendingDuration(duration),
      "limit": limit
    }

    self._check_rate_limit()
    op = self._run_op()
    try:
      op.books_trending(**arguments)
      # implement type checking
      raw = self._client(op)
      res = op + raw

      tb = res.books_trending
      TrendingBooks.model_validate(tb.__to_json_value__())

      return res
    except GraphQLErrors as ex:
      logger.error("GraphQLError: %s" % ex.errors)
    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)

  def user_books_progress(
    self,
    limit: int = 25
  ):
    if limit > self._query_limit:
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    self._check_rate_limit()
    op = self._run_op()
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
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)

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
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    self._check_rate_limit()
    op = self._run_op()
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
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)

  def platforms(
    self,
    platform_id: int | None = None,
    limit: int | None = 25,
    offset: int | None = 0
  ):
    if limit > self._query_limit:
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    order_by = platforms_order_by({"id": ORDER_BY("asc")})
    arguments = {
      "limit": limit,
      "order_by": [order_by]
    }
    if isinstance(platform_id, int):
      arguments["where"] = {"id": {"_eq": platform_id}}

    self._check_rate_limit()
    op = self._run_op()
    try:
      op.platforms(**arguments)
      op.platforms.__fields__("id", "name", "url")
      raw = self._client(op)
      if raw.get("errors"):
        raise GraphQLErrors(errors=raw["errors"], data=raw.get("data"))
      res = op + raw

      for i in res.platforms:
        Platform.model_validate(i.__to_json_value__())

      if self._return_json:
        json = res.__to_json_value__()
        return json
      else:
        return res

    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
      return None
    except ValueError as e:
      logger.error("ValueError: %s" % e)
      return None

  def publishers(
    self,
    publisher_name: str | None = None,
    limit: int = 25,
    offset: int = 0
  ):
    if limit > self._query_limit:
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

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

    self._check_rate_limit()
    op = self._run_op()
    publisher_fields = Publisher.model_fields.keys()
    try:
      op.publishers(**arguments)
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
      logger.error("ValidationError: %s" % e)
      return None
    except ValueError as e:
      logger.error("ValueError: %s" % e)
      return None

  def reading_journals(
    self,
    user_id: int,
    limit: int = 10,
    offset: int = 0,
    sort: Literal["asc", "desc"] = "desc",
  ):
    if limit > self._query_limit:
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    where = {"user_id": {"_eq": user_id}}
    order_by = reading_journals_order_by({"action_at": ORDER_BY(sort)})
    arguments = {
      "where": {**where},
      "limit": limit,
      "offset": offset,
      "order_by": [order_by] # NOTE: order_by argument is expected as a list_of
    }

    self._check_rate_limit()
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
      logger.error("ValidationError: %s" % e)
      return None
    except ValueError as e:
      logger.error("ValueError: %s" % e)
      return None

  #### SEARCH FIELD POWERED
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
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    arguments = {
      "query": search,
      "query_type": "author",
      "per_page": limit
    }
    if offset:
      arguments["offset"] = offset

    self._check_rate_limit()
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
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)

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
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    # NOTE: include possible update for more customizable search params
    arguments = {
      "query": search,
      "query_type": "book",
      "per_page": limit
    }
    if offset:
      arguments["offset"] = offset

    self._check_rate_limit()
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
    except GraphQLErrors as ex:
      logger.error("GraphQLError: %s" % ex.errors)
    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)

  def characters(
    self,
    character_name: str,
    limit: int = 10,
    offset: int = 0
  ):
    if limit > self._query_limit:
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    arguments = {
      "query": character_name,
      "query_type": "Character",
      "per_page": limit,
      "page": 1
    }

    self._check_rate_limit()
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

      # for doc in hits:
      #   Series.model_validate(doc['document'])

      if self._return_json:
        json = res.__to_json_value__()
        return json
      else:
        return re
    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
      return None
    except ValueError as e:
      logger.error("ValueError: %s" % e)
      return None

  def lists(
    self,
    list_name: str,
    limit: int = 10,
    offset: int = 0
  ):
    if limit > self._query_limit:
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    arguments = {
      "query": list_name,
      "query_type": "List",
      "per_page": limit
    }

    # figure out per_page issue
    self._check_rate_limit()
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

      # for doc in hits:
      #   Series.model_validate(doc['document'])

      if self._return_json:
        json = res.__to_json_value__()
        return json
      else:
        return re

    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
      return None
    except ValueError as e:
      logger.error("ValueError: %s" % e)
      return None

  def series(
    self,
    search: str,
    limit: int = 10,
    offset: int = 0
  ):
    """Search series from database.

    Args:
      search (str): Query string to be used for search.
      limit (int): Number of results.
      offset (int): Skip n results.

    Returns:
      hits (list): List of matching series.
    """
    if limit > self._query_limit:
      logger.warning("Query request exceeds limit, setting to limit...")
      limit = self._query_limit

    arguments = {
      "query": search,
      "query_type": "series",
      "per_page": limit
    }
    if offset:
      arguments["offset"] = offset

    self._check_rate_limit()
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
        return re
    except ValidationError as e:
      logger.error("ValidationError: %s" % e)
    except ValueError as e:
      logger.error("ValueError: %s" % e)