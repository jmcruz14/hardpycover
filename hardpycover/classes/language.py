from pydantic import BaseModel

class Language(BaseModel):
  code2: str | None = None
  code3: str | None = None
  id: int | None = None
  language: str | None = None
