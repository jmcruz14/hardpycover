from pydantic import BaseModel


class BookCategory(BaseModel):
	id: int | None = None
	name: str | None = None
