from datetime import datetime
from pydantic import BaseModel


class Publisher(BaseModel):
	id: int | None = (None,)
	created_at: datetime | None = None
	updated_at: datetime | None = None
	slug: str | None = None
	name: str | None = None
	editions_count: int | None = None


class ParentPublisher(Publisher):
	parent_publisher: Publisher | None = None
