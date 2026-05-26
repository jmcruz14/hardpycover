from datetime import datetime, date
from typing import Optional, Annotated
from pydantic import BaseModel

class SumAvgStdFields(BaseModel):
  """
    List of available fields for use in the `avg` table of the API. 
  """
  book_id: Optional[int | float] = None
  edition_id: Optional[int | float] = None
  id: Optional[int | float] = None
  likes_count: Optional[int | float] = None
  original_book_id: Optional[int | float] = None
  original_edition_id: Optional[int | float] = None
  rating: Optional[int | float] = None
  read_count: Optional[int | float] = None
  referrer_user_id: Optional[int | float] = None
  review_length: Optional[int | float] = None
  user_id: Optional[int | float] = None

class MaxMinFields(BaseModel):
  """
    List of available fields for use in the `max/min` table of the API.
  """
  book_id: Optional[int | float] = None
  created_at: Optional[datetime] = None
  date_added: Optional[date] = None
  edition_id: Optional[int] = None
  first_read_date: Optional[date] = None
  first_started_reading_date: Optional[date] = None
  id: Optional[int] = None
  last_read_date: Optional[date] = None
  likes_count: Optional[int] = None
  merged_at: Optional[datetime] = None
  owned_copies: Optional[int] = None
  rating: Optional[int] = None
  read_count: Optional[int] = None
  review: Optional[Annotated[str, "Review text with HTML tags"]] = None
  review_length: Optional[int] = None
  review_raw: Optional[Annotated[str, "Review text without HTML tags"]] = None
  updated_at: Optional[datetime] = None
  user_id: Optional[int] = None

class AggregateStats(BaseModel):
  avg: Optional[SumAvgStdFields] = None
  count: Optional[int] = None
  max: Optional[MaxMinFields] = None
  min: Optional[MaxMinFields] = None
  stddev: Optional[SumAvgStdFields] = None
  sum: Optional[SumAvgStdFields] = None

  # basic: max, min, stddev

class UserBooksAggregate(BaseModel):
  aggregate: Optional[AggregateStats] = None
  # NOTE: nodes support currently on hold