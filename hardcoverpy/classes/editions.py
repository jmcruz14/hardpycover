from datetime import datetime, date
from typing import Optional, Literal
from pydantic import BaseModel

from .language import Language
from .publishers import Publisher

class Edition(BaseModel):
  title: Optional[str] = None
  subtitle: Optional[str] = None
  state: Optional[str] = None # normalized, duplicate, ???
  score: Optional[int] = None
  edition: Optional[str] = None
  edition_format: Optional[str] = None
  edition_information: Optional[str] = None
  language_id: Optional[int] = None
  language: Optional[Language] = None
  country_id: Optional[int] = None
  image_id: Optional[int] = None
  publisher_id: Optional[int] = None
  publisher: Optional[Publisher] = None
  pages: Optional[int] = None
  isbn_10: Optional[str] = None
  isbn_13: Optional[str] = None
  lists_count: Optional[int] = None
  object_type: Optional[Literal['Edition']] = None
  release_year: Optional[int] = None
  release_date: Optional[date] = None
  users_count: Optional[int] = None
  users_read_count: Optional[int] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  # normalized_at: Optional[datetime] = None