from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel

from .books import Book
from .editions import Edition

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
  sponsored_review: Optional[bool] = None
  url: Optional[str] = None
  updated_at: Optional[datetime] = None
  user_id: Optional[int] = None