from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field


class Character(BaseModel):
	character_id: int | None = Field(default=None, alias="id")
	name: str | None = None
	biography: str | None = None
	books_count: int | None = None
	canonical_books_count: int | None = None
	created_at: datetime | None = None
	updated_at: datetime | None = None
	has_disability: bool | None = None
	is_lgbtq: bool | None = None
	is_poc: bool | None = None
	image_id: str | None = None
	state: str | None = None
	slug: str | None = None
	object_type: Literal["Character"] | None = None
	gender_id: int | None = None
	user_id: str | None = None
