from __future__ import annotations # prevents eager loading upon import
from pydantic import BaseModel, ValidationInfo, Field, field_validator
from typing import Literal
from typing_extensions import TypedDict
from datetime import datetime

from .author import Author
from .utils import Identifiers
from .books import Book

# NOTE: this is an intermediate table bridging book to series
class BookSeries(BaseModel):
  """
    Intermediate table bridging `Book` to `Series`. Contains
    information about the relationship of book to series.
  """

  book: Book | None = None
  book_id: int | None = None
  compilation: bool | None = None
  created_at: datetime | None = None
  details: str | None = None
  featured: bool | None = None
  book_series_id: int | None = Field(default=None, alias="id")
  position: float | None = None
  series_id: int | None = None
  series: Series | None = None # noqa: F821
  updated_at: datetime | None = None

  @field_validator('position', mode='after')
  def validate_position_details(cls, info: ValidationInfo):
    coerced_detail_num = float(info.data['details'])
    if coerced_detail_num != info.data['position']:
      raise ValueError("Positions do not match")

class Series(BaseModel):
  author_id: int | None = None
  author: Author | None = None
  book_series: list[BookSeries] | None = None
  # type: ignore
  books_count: int | None = None
  # canonical?
  canonical_id: int | None = None
  series_id: int | None = Field(default=None, alias="id")
  identifiers: Identifiers | None = None
  is_completed: bool | None = None
  locked: bool | None = None
  name: str | None = None
  object_type: Literal["Series"] | None = None
  primary_books_count: int | None = None
  slug: str | None = None
  state: Literal["active", "duplicate"] | None = None
  user_id: int | None = None

BookSeries.model_rebuild() # ForwardRef for the book_series `BookSeries` field