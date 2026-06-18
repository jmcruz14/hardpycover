from pydantic import BaseModel, Field

class BookCategory(BaseModel):
	book_category_id: int | None = Field(default=None, alias="id")
	name: str | None = None
