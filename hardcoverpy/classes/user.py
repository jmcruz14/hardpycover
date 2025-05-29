from typing import Optional, Literal, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# NOTE: expand the User class accordingly
class User(BaseModel):
  id: Optional[int] = None
  bio: Optional[str] = None
  birthdate: Optional[str] = None
  books_count: Optional[int] = None
  created_at: Optional[datetime] = None
  email: Optional[str] = None
  image_id: Optional[int] = None
  last_activity_at: Optional[datetime] = None
  last_sign_in_at: Optional[datetime] = None
  librarian_roles: Optional[List[str]] = None # literal but which values? (appender, editor, librarian)
  object_type: Optional[Literal['User']] = None
  username: Optional[str] = None