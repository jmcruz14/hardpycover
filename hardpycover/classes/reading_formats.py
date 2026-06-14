from pydantic import BaseModel

class ReadingFormat(BaseModel):
  format: str
  id: int