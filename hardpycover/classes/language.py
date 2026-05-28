from typing import Optional
from pydantic import BaseModel

class Language(BaseModel):
  code2: Optional[str] = None
  code3: Optional[str] = None
  id: Optional[int] = None
  language: Optional[str] = None