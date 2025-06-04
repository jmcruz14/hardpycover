from typing import Optional, Literal, Dict, List
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict

class Character(BaseModel):
  id: Optional[int] = None
  name: Optional[str] = None
  biography: Optional[str] = None
  books_count: Optional[int] = None
  canonical_books_count: Optional[int] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  has_disability: Optional[bool] = None
  is_lgbtq: Optional[bool] = None
  is_poc: Optional[bool] = None
  image_id: Optional[str] = None
  state: Optional[str] = None
  slug: Optional[str] = None
  object_type: Optional[Literal['Character']] = None
  gender_id: Optional[int] = None
  user_id: Optional[str] = None