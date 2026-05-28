from typing import Optional, Dict, List
from datetime import date
from pydantic import BaseModel

from .image import CachedImage
from .utils import Identifiers, Link

class Author(BaseModel):
  alternate_names: Optional[List[str]] = None
  alias_id: Optional[int] = None
  bio: Optional[str] = None
  books_count: Optional[int] = None
  born_date: Optional[date] = None
  born_year: Optional[int] = None
  cached_image: Optional[CachedImage] = None
  canonical_id: Optional[int] = None
  death_date: Optional[date] = None
  death_year: Optional[int] = None
  gender_id: Optional[int] = None
  id: Optional[int] = None
  identifiers: Optional[Identifiers] = None
  image_id: Optional[int] = None
  is_bipoc: Optional[bool] = None
  is_lgbtq: Optional[bool] = None
  links: Optional[List[Link]] = None
  location: Optional[str] = None
  locked: Optional[bool] = None
  name: Optional[str] = None
  name_personal: Optional[str] = None
  slug: Optional[str] = None
  state: Optional[str] = None
  title: Optional[str] = None
  user_id: Optional[int] = None
  users_count: Optional[int] = None
