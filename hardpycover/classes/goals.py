from pydantic import BaseModel
from datetime import datetime, date
from typing import Literal

class Goal(BaseModel):
  archived: bool | None = None
  completed_at: datetime | None = None
  # conditions
  description: str | None = None
  start_date: date | None = None
  end_date: date | None = None
  # followers
  goal: int | None = None
  id: int | None = None
  metric: Literal["book", "hour", "page"] | None = None
  privacy_setting_id: Literal[1,2,3] | None = None
  progress: int | None = None
  state: Literal["active", "completed", "failed"] | None = None
  user_id: int | None = None