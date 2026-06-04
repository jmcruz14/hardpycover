from typing import Optional, Literal, List
from datetime import datetime, date
from pydantic import BaseModel
from .utils import CachedImage

# NOTE: expand the User class accordingly
class User(BaseModel):
  id: Optional[int] = None
  bio: Optional[str] = None
  cached_image: Optional[CachedImage] = None
  birthdate: Optional[str] = None
  books_count: Optional[int] = None
  created_at: Optional[datetime] = None
  email: Optional[str] = None
  followers_count: Optional[int] = None
  followed_users_count: Optional[int] = None
  image_id: Optional[int] = None
  last_activity_at: Optional[datetime] = None
  last_sign_in_at: Optional[datetime] = None
  librarian_roles: Optional[List[str]] = None # literal but which values? (appender, editor, librarian)
  object_type: Optional[Literal['User']] = None
  username: Optional[str] = None
  updated_at: Optional[datetime] = None

class UserStatus(BaseModel):
  id: Optional[int] = None
  status: Optional[Literal["created", "activated", "banned"]] = None

class Me(BaseModel):
  id: Optional[int] = None
  access_level: Optional[int] = None
  account_privacy_setting_id: Optional[int] = None
  activity_privacy_settings_id: Optional[int] = None
  admin: Optional[bool] = False
  bio: Optional[str] = None
  birthdate: Optional[str | date] = None
  books_count: Optional[int] = None
  cached_cover: Optional[CachedImage] = None
  cached_image: Optional[CachedImage] = None
  confirmed_at: Optional[datetime] = None
  confirmation_sent_at: Optional[datetime] = None
  created_at: Optional[datetime] = None
  current_sign_in_at: Optional[datetime] = None
  default_reading_format_id: Optional[int] = None
  email: Optional[str] = None
  email_verified: Optional[bool] = None
  followers_count: Optional[int] = None
  followed_users_count: Optional[int] = None
  image_id: Optional[int] = None
  last_activity_at: Optional[datetime] = None
  last_sign_in_at: Optional[datetime] = None
  librarian_roles: Optional[List[str]] = None # literal but which values? (appender, editor, librarian)
  location: Optional[str] = None
  object_type: Optional[Literal['User']] = None
  username: Optional[str] = None
  updated_at: Optional[datetime] = None
  timezone: Optional[str] = None
  status_id: Optional[int] = None
  sign_in_count: Optional[int] = None
  referrer_url: Optional[str] = None
  pronoun_possessive: Optional[str] = None
  pronoun_personal: Optional[str] = None