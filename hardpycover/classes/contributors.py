from datetime import datetime
from pydantic import BaseModel

from .author import Author


class Contributor(BaseModel):
	author_id: int | None = None
	contributable_type: str | None = None  # Could be a literal
	contributable_id: int | None = None
	contribution: str | None = None  # Could be literal
	created_at: datetime | None = None
	id: int
	updated_at: datetime | None = None


class CachedContributor(BaseModel):
	author: Author | None = None
	contribution: str | None = None


# NOTE: list of contribution literals
# book, afterword, design, ...
# null, Contributor, Translator, translator
