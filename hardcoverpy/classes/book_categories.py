from typing import Optional
from pydantic import BaseModel

class BookCategory(BaseModel):
  id: Optional[int] = None
  name: Optional[str] = None