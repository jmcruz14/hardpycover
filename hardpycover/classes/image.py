from pydantic import BaseModel, Field


class Image(BaseModel):
	color: str | None = None
	colors: list[str] | None = None
	height: int | None = None
	imageable_id: int | None = None
	image_id: int | None = Field(default=None, alias="id")
	imageable_type: str | None = None
	ratio: int | None = None
	url: str | None = None
	width: int | None = None


class CachedImage(Image):
	pass
