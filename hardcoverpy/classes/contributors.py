from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class Contributor(BaseModel):
  author_id: Optional[int] = None
  contributable_type: Optional[str] = None # Could be a literal
  contributable_id: Optional[int] = None
  contribution: Optional[str] = None # Could be literal
  created_at: Optional[datetime] = None
  id: int
  updated_at: Optional[datetime] = None

# NOTE: list of contribution literals
# book, afterword, design, ...