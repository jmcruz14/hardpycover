from pydantic import BaseModel, Field
from datetime import datetime
from .utils import PrivacySetting

from .user import User

class Prompt(BaseModel):
  answers_count: int | None = None
  books_count: int | None = None
  created_at: datetime | None = None
  description: str | None = None
  featured: bool | None = None
  # followed_prompts, followers
  prompt_id: int | None = Field(default=None, alias="id")
  privacy_setting: PrivacySetting | None = None
  privacy_setting_id: int | None = None
  question: str | None = None
  slug: str | None = None
  user: User | None = None
  user_id: int | None = None
  users_count: int | None = None