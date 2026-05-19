from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict

class Publisher(BaseModel):
  id: Optional[int] = None,
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  slug: Optional[str] = None
  name: Optional[str] = None
  editions_count: Optional[int] = None

class ParentPublisher(Publisher):
  parent_publisher: Optional[Publisher] = None