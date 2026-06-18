from pydantic import BaseModel, Field

class ReadingFormat(BaseModel):
  format: str
  reading_format_id: int | None = Field(default=None, alias="id")