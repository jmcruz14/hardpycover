from datetime import datetime
from pydantic import BaseModel, Field


class Publisher(BaseModel):
	publisher_id: int | None = Field(default=None, alias="id")
	created_at: datetime | None = None
	updated_at: datetime | None = None
	slug: str | None = None
	name: str | None = None
	editions_count: int | None = None


class ParentPublisher(Publisher):
	parent_publisher: Publisher | None = None
