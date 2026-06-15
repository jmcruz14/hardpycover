from typing import Literal, Annotated
from datetime import datetime, date
from pydantic import BaseModel

from .books import Book
from .editions import Edition


class UserBookReads(BaseModel):
	id: int | None = None
	edition: Edition | None = None
	edition_id: int | None = None
	started_at: date | None = None
	finished_at: date | None = None
	user_book_id: int | None = None
	progress: Annotated[int | None, "percent done expressed as integer"] = None
	progress_pages: int | None = None
	progress_seconds: int | None = None


class UserBook(BaseModel):
	book_id: int | None = None  # matches book id; separate from user_books_id (id)
	book: Book | None = None
	created_at: datetime | None = None
	date_added: date | None = None
	edition_id: int | None = None
	edition: Edition | None = None
	first_read_date: date | None = None
	first_started_reading_date: date | None = None
	id: int | None = None
	has_review: bool | None = None
	imported: bool | None = None  #
	last_read_date: date | None = None
	likes_count: int | None = None
	merged_at: datetime | None = None
	media_url: str | None = None
	object_type: "UserBook | None" = None
	original_book_id: int | None = None
	original_edition_id: int | None = None
	owned: bool | None = None
	owned_copies: int | None = None
	privacy_setting_id: int | None = None
	read_count: int | None = None
	reading_format_id: int | None = None
	recommended_for: str | None = None
	recommended_by: str | None = None
	referrer_user_id: int | None = None
	review: str | None = None
	review_raw: str | None = None
	review_has_spoilers: bool | None = None
	review_migrated: bool | None = None
	review_length: int | None = None
	rating: int | float | None = None
	starred: bool | None = None
	# NOTE: 1 - Want to read; 2 - Currently Reading; 3 - Read
	# 4 - Paused; 5 - DNF; 6 - Ignored
	status_id: Literal[1, 2, 3, 4, 5, 6] | None = None
	sponsored_review: bool | None = None
	url: str | None = None
	updated_at: datetime | None = None  # explore way to convert datetime into str and vv
	user_id: int | None = None
	user_book_reads: UserBookReads | None = None


class UserBookStats(BaseModel):
	id: Literal[1, 2, 3, 4, 5, 6] | None = None
	description: str | None = None
	slug: str | None = None
	status: str | None = None
