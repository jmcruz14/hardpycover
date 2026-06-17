from typing import Literal
from datetime import datetime, date
from pydantic import BaseModel


class RatingsDistribution(BaseModel):
	count: int
	rating: int


class Book(BaseModel):
	id: int | None = None
	image_id: int | None = None
	description: str | None = None
	default_physical_edition_id: int | None = None
	default_ebook_edition_id: int | None = None
	default_cover_edition_id: int | None = None
	default_audio_edition_id: int | None = None
	activities_count: int | None = None
	alternative_titles: str | list[str] | None = None
	book_category_id: int | None = None
	content_warnings: list[str] | None = None
	created_by_user_id: int | None = None
	users_read_count: int | None = None
	users_count: int | None = None
	user_added: bool | None = None
	updated_at: datetime | None = None
	title: str | None = None
	subtitle: str | None = None
	state: Literal["error", "pending", "normalized", "duplicate"] | None = (
		None  # This is a Literal but we need to confirm w/c values
	)
	slug: str | None = None
	ratings_distribution: list[RatingsDistribution] | None = None
	ratings_count: int | None = None
	rating: int | float | None = None
	prompts_count: int | None = None
	release_date: date | None = None
	release_year: int | None = None
	reviews_count: int | None = None


class SearchBookDocument(BaseModel):
	activities_count: int | None = None
	alternative_titles: str | None = None
	audio_seconds: int | None = None
	author_names: list[str] | None = None
	compilation: bool | None = None
	content_warnings: list[str] | None = None
	contribution_types: list[str] | None = None
	description: str | None = None
	genres: list[str] | None = None
	isbns: list[int] | None = None
	has_audiobook: bool | None = None
	has_ebook: bool | None = None
	moods: list[str] | None = None
	pages: int | None = None
	prompts_count: int | None = None
	rating: float | None = None
	ratings_count: int | None = None
	release_date: date | None = None
	release_year: int | None = None
	reviews_count: int | None = None
	series_ids: list[int] | None = None
	series_names: list[str] | None = None
	slug: str | None = None
	tags: list[str] | None = None
	title: str | None = None
	users_count: int | None = None
	users_read_count: int | None = None

class TrendingBooks(BaseModel):
	error: str | None = None
	ids: list[int] | None = None