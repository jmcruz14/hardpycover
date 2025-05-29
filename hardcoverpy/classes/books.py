from typing import Optional, Literal, List
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict

class RatingsDistribution(BaseModel):
  count: int
  rating: int

class Book(BaseModel):
  id: Optional[int] = None
  image_id: Optional[int] = None
  description: Optional[str] = None
  default_physical_edition_id: Optional[int] = None
  default_ebook_edition_id: Optional[int] = None
  default_cover_edition_id: Optional[int] = None
  default_audio_edition_id: Optional[int] = None
  created_by_user_id: Optional[int] = None
  book_category_id: Optional[int] = None
  users_read_count: Optional[int] = None
  users_count: Optional[int] = None
  user_added: Optional[bool] = None
  updated_at: Optional[datetime] = None
  title: Optional[str] = None
  subtitle: Optional[str] = None
  state: Optional[Literal['error', 'pending', 'normalized', 'duplicate']] = None # This is a Literal but we need to confirm w/c values
  slug: Optional[str] = None
  ratings_distribution: Optional[List[RatingsDistribution]]
  ratings_count: Optional[int] = None
  rating: Optional[int | float] = None
  prompts_count: Optional[int] = None
  release_date: Optional[date] = None
  release_year: Optional[int] = None
  reviews_count: Optional[int] = None
  users_count: Optional[int] = None
  users_read_count: Optional[int] = None