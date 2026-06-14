from pydantic import BaseModel
from typing import Annotated, Literal
from datetime import datetime

class Lists(BaseModel):
  books: Annotated[list[str] | None, "array of strings of listed books"] = None
  books_count: int | None = None
  created_at: datetime | None = None
  default_view: Literal["card", "table", "shelf"] | None = None
  description: str | None = None
  featured: bool | None = None
  featured_profile: bool | None = None
  followers_count: int | None = None
  id: int | None = None
  imported: bool | None = None
  likes_count: int | None = None
  name: str | None = None
  object_type: Literal["List"] | None = None
  privacy_setting_id: int | None = None
  public: bool | None = None
  ranked: bool | None = None
  slug: str | None = None
  updated_at: datetime | None = None
  url: str | None = None
  user_id: int | None = None