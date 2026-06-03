from datetime import date
from typing import Optional
from pydantic import BaseModel

class SumAvgStdFields(BaseModel):
  edition_id: Optional[int | float] = None
  finished_at_precision: Optional[int | float] = None
  id: Optional[int | float] = None
  progress: Optional[int | float] = None
  progress_pages: Optional[int | float] = None
  progress_seconds: Optional[int | float] = None
  user_book_id: Optional[int | float] = None
 
class MaxMinFields(BaseModel):
  edition_id: Optional[int | float] = None
  finished_at: Optional[date] = None
  finished_at_precision: Optional[int | float] = None
  id: Optional[int | float] = None
  # NOTE: paused_at tbd
  progress: Optional[int | float] = None
  progress_pages: Optional[int | float] = None
  progress_seconds: Optional[int | float] = None
  started_at: Optional[date] = None
  user_book_id: Optional[int | float] = None

class AggregateStats(BaseModel):
  avg: Optional[SumAvgStdFields] = None
  count: Optional[int] = None
  max: Optional[MaxMinFields] = None
  min: Optional[MaxMinFields] = None
  stddev: Optional[SumAvgStdFields] = None
  sum: Optional[SumAvgStdFields] = None
  # basic: max, min, stddev

class UserBookReadsAggregate(BaseModel):
  aggregate: Optional[AggregateStats] = None