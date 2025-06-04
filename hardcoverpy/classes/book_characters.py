from typing import Optional, Literal
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict

from .characters import Character
from .books import Book

class BookCharacter(BaseModel):
  id: Optional[int] = None
  book: Optional[Book] = None
  book_id: Optional[int] = None
  character: Optional[Character] = None
  character_id: Optional[int] = None
  only_mentioned: Optional[bool] = None
  position: Optional[int] = None
  spoiler: Optional[bool] = None