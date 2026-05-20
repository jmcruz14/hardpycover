from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Publisher(BaseModel):
  id: Optional[int] = None,
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  slug: Optional[str] = None
  name: Optional[str] = None
  editions_count: Optional[int] = None

class ParentPublisher(Publisher):
  parent_publisher: Optional[Publisher] = None