from pydantic import BaseModel, Field

from .characters import Character
from .books import Book


class BookCharacter(BaseModel):
	book_character_id: int | None = Field(default=None, alias="id")
	book: Book | None = None
	book_id: int | None = None
	character: Character | None = None
	character_id: int | None = None
	only_mentioned: bool | None = None
	position: int | None = None
	spoiler: bool | None = None
