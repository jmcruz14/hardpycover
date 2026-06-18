from datetime import date
from pydantic import BaseModel, Field

from .image import CachedImage
from .utils import Identifiers, Link


class Author(BaseModel):
	alternate_names: list[str] | None = None
	alias_id: int | None = None
	books: list[str] | None = None  # NOTE: exclusive to search results only
	bio: str | None = None
	books_count: int | None = None
	born_date: date | None = None
	born_year: int | None = None
	cached_image: CachedImage | None = None
	canonical_id: int | None = None
	death_date: date | None = None
	death_year: int | None = None
	gender_id: int | None = None
	author_id: int | None = Field(default=None, alias="id")
	identifiers: Identifiers | None = None
	image_id: int | None = None
	is_bipoc: bool | None = None
	is_lgbtq: bool | None = None
	links: list[Link] | None = None
	location: str | None = None
	locked: bool | None = None
	name: str | None = None
	name_personal: str | None = None
	series_names: list[str] | None = None  # NOTE: exclusive to search results only
	slug: str | None = None
	state: str | None = None
	title: str | None = None
	user_id: int | None = None
	users_count: int | None = None
