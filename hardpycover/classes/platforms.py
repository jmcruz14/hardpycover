from pydantic import BaseModel, AnyHttpUrl, Field

class Platform(BaseModel):
  platform_id: int | None = Field(default=None, alias="id")
  name: str | None = None
  url: AnyHttpUrl | None = None
  # book_mappings: list[BookMappings] | None = None