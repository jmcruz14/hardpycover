from pydantic import BaseModel, AnyHttpUrl

class Platform(BaseModel):
  id: int | None = None
  name: str | None = None
  url: AnyHttpUrl | None = None
  # book_mappings: list[BookMappings] | None = None