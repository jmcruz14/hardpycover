from pydantic import BaseModel, Field


class Language(BaseModel):
	code2: str | None = None
	code3: str | None = None
	language_id: int | None = Field(default=None, alias="id")
	language: str | None = None
