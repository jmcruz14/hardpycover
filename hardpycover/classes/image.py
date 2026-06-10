from pydantic import BaseModel

class Image(BaseModel):
  color: str | None = None
  colors: list[str] | None = None
  height: int | None = None
  imageable_id: int | None = None
  id: int | None = None
  imageable_type: str | None = None
  ratio: int | None = None
  url: str | None = None
  width: int | None = None

class CachedImage(Image):
  pass
