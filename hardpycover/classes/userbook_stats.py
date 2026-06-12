from datetime import date
from pydantic import BaseModel


class SumAvgStdFields(BaseModel):
	edition_id: int | float | None = None
	finished_at_precision: int | float | None = None
	id: int | float | None = None
	progress: int | float | None = None
	progress_pages: int | float | None = None
	progress_seconds: int | float | None = None
	user_book_id: int | float | None = None


class MaxMinFields(BaseModel):
	edition_id: int | float | None = None
	finished_at: date | None = None
	finished_at_precision: int | float | None = None
	id: int | float | None = None
	# NOTE: paused_at tbd
	progress: int | float | None = None
	progress_pages: int | float | None = None
	progress_seconds: int | float | None = None
	started_at: date | None = None
	user_book_id: int | float | None = None


class AggregateStats(BaseModel):
	avg: SumAvgStdFields | None = None
	count: int | None = None
	max: MaxMinFields | None = None
	min: MaxMinFields | None = None
	stddev: SumAvgStdFields | None = None
	sum: SumAvgStdFields | None = None
	# basic: max, min, stddev


class UserBookReadsAggregate(BaseModel):
	aggregate: AggregateStats | None = None
