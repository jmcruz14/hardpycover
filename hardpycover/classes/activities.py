from pydantic import BaseModel
from datetime import datetime
from typing import Literal

from .books import Book
from .userbooks import UserBook
from .prompts import Prompt
from .goals import Goal
from .lists import Lists
from .utils import PrivacySetting

class Activities(BaseModel):
  # book: Book | None = None
  book_id: int | None = None
  created_at: datetime | None = None
  data: UserBook | Prompt | Goal | Lists | None = None
  event: Literal["UserBookActivity", "GoalActivity", "PromptActivity", "ListActivity"] | None = None
  id: int | None = None
  # likes:
  likes_count: int | None = None
  object_type: Literal["Activity"] | None = None
  original_book_id: int | None = None
  privacy_setting: PrivacySetting | None = None # NOTE: currently disabling this to prevent nested queries
  privacy_setting_id: Literal[1,2,3] | None = None
  uid: str | None = None # unique string for dedup
  user_id: int | None = None