from datetime import datetime, date
from typing import Literal
from pydantic import BaseModel

from .language import Language
from .publishers import Publisher

class Edition(BaseModel):
  title: str | None = None
  subtitle: str | None = None
  state: str | None = None # normalized, duplicate, ???
  score: int | None = None
  edition: str | None = None
  edition_format: str | None = None
  edition_information: str | None = None
  language_id: int | None = None
  language: Language | None = None
  country_id: int | None = None
  image_id: int | None = None
  publisher_id: int | None = None
  publisher: Publisher | None = None
  pages: int | None = None
  isbn_10: str | None = None
  isbn_13: str | None = None
  lists_count: int | None = None
  object_type: Literal['Edition'] | None = None
  release_year: int | None = None
  release_date: date | None = None
  users_count: int | None = None
  users_read_count: int | None = None
  created_at: datetime | None = None
  updated_at: datetime | None = None
  # normalized_at: datetime | None = None
