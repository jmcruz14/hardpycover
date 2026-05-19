from typing import Optional, Literal
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict

class BookCategory(BaseModel):
  id: Optional[int] = None
  name: Optional[str] = None