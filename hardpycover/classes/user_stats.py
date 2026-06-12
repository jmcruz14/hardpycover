from datetime import datetime, date
from typing import Annotated
from pydantic import BaseModel


class SumAvgStdFields(BaseModel):
	"""
	List of available fields for use in the `avg` table of the API.
	"""

	book_id: int | float | None = None
	edition_id: int | float | None = None
	id: int | float | None = None
	likes_count: int | float | None = None
	original_book_id: int | float | None = None
	original_edition_id: int | float | None = None
	rating: int | float | None = None
	read_count: int | float | None = None
	referrer_user_id: int | float | None = None
	review_length: int | float | None = None
	user_id: int | float | None = None


class MaxMinFields(BaseModel):
	"""
	List of available fields for use in the `max/min` table of the API.
	"""

	book_id: int | float | None = None
	created_at: datetime | None = None
	date_added: date | None = None
	edition_id: int | None = None
	first_read_date: date | None = None
	first_started_reading_date: date | None = None
	id: int | None = None
	last_read_date: date | None = None
	likes_count: int | None = None
	merged_at: datetime | None = None
	owned_copies: int | None = None
	rating: int | None = None
	read_count: int | None = None
	review: Annotated[str, "Review text with HTML tags"] | None = None
	review_length: int | None = None
	review_raw: Annotated[str, "Review text without HTML tags"] | None = None
	updated_at: datetime | None = None
	user_id: int | None = None


class AggregateStats(BaseModel):
	avg: SumAvgStdFields | None = None
	count: int | None = None
	max: MaxMinFields | None = None
	min: MaxMinFields | None = None
	stddev: SumAvgStdFields | None = None
	sum: SumAvgStdFields | None = None

	# basic: max, min, stddev


class UserBooksAggregate(BaseModel):
	aggregate: AggregateStats | None = None
	# NOTE: nodes support currently on hold
