from .books import Book
from .editions import Edition
from datetime import datetime
from pydantic import BaseModel
from typing import Literal

class ReadingJournal(BaseModel):
  action_at: datetime | None = None
  book_id: int | None = None
  book: Book | None = None
  created_at: datetime | None = None
  edition_id: int | None = None
  edition: Edition | None = None
  entry: str | None = None
  event: str | None = None
  id: int | None = None
  likes_count: int | None = None
  # metadata
  object_type: Literal["ReadingJournal"] | None = None
  privacy_setting_id: int | None = None
  updated_at: datetime | None = None
  user_id: int | None = None
