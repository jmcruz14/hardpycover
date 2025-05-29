from typing import Optional, Literal, List
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict

class Image(BaseModel):
  color: Optional[str] = None
  colors: Optional[List[str]] = None
  height: Optional[int] = None
  imageable_id: Optional[int] = None
  id: Optional[int] = None
  imageable_type: Optional[str] = None
  ratio: Optional[int] = None
  url: Optional[str] = None
  width: Optional[int] = None