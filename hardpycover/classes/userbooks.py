from typing import Optional, Literal, Annotated
from datetime import datetime, date
from pydantic import BaseModel

from .books import Book
from .editions import Edition

class UserBookReads(BaseModel):
  id: Optional[int] = None
  edition: Optional[Edition] = None
  edition_id: Optional[int] = None
  started_at: Optional[date] = None
  finished_at: Optional[date] = None
  user_book_id: Optional[int] = None
  progress: Annotated[Optional[int], "percent done expressed as integer"] = None
  progress_pages: Optional[int] = None
  progress_seconds: Optional[int] = None

class UserBook(BaseModel):
  book_id: Optional[int] = None # matches book id; separate from user_books_id (id)
  book: Optional[Book] = None
  created_at: Optional[datetime] = None
  date_added: Optional[date] = None
  edition_id: Optional[int] = None
  edition: Optional[Edition] = None
  first_read_date: Optional[date] = None
  first_started_reading_date: Optional[date] = None
  id: Optional[int] = None
  has_review: Optional[bool] = None
  imported: Optional[bool] = None #
  last_read_date: Optional[date] = None
  likes_count: Optional[int] = None
  merged_at: Optional[datetime] = None
  media_url: Optional[str] = None
  object_type: Optional['UserBook'] = None
  original_book_id: Optional[int] = None
  original_edition_id: Optional[int] = None
  owned: Optional[bool] = None
  owned_copies: Optional[int] = None
  privacy_setting_id: Optional[int] = None
  read_count: Optional[int] = None
  reading_format_id: Optional[int] = None
  recommended_for: Optional[str] = None
  recommended_by: Optional[str] = None
  referrer_user_id: Optional[int] = None
  review: Optional[str] = None
  review_has_spoilers: Optional[bool] = None
  rating: Optional[int | float] = None
  starred: Optional[bool] = None
  # NOTE: 1 - Want to read; 2 - Currently Reading; 3 - Read
  # 4 - Paused; 5 - DNF; 6 - Ignored
  status_id: Optional[Literal[1,2,3,4,5,6]] = None
  sponsored_review: Optional[bool] = None
  url: Optional[str] = None
  updated_at: Optional[datetime] = None # explore way to convert datetime into str and vv
  user_id: Optional[int] = None
  user_book_reads: Optional[UserBookReads] = None

class UserBookStats(BaseModel):
  id: Optional[Literal[1,2,3,4,5,6]] = None
  description: Optional[str] = None
  slug: Optional[str] = None
  status: Optional[str] = None