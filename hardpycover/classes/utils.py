from pydantic import BaseModel


class Image(BaseModel):
	id: int
	url: str
	color: str
	width: int
	height: int
	color_name: str


class CachedImage(Image):
	pass


class LinkType(BaseModel):
	key: str


class Link(BaseModel):
	url: str
	type: LinkType
	title: str


class Identifiers(BaseModel):
	goodreads: list[str] | str | None = None
	openlibrary: list[str] | str | None = None


class MatchedTokens(BaseModel):
	matched_tokens: list[str] | None = None
	snippet: str | None = None


class TextMatchInfo(BaseModel):
	best_field_score: str | None = None  # String representation of an int value
	best_field_weight: int | None = None
	fields_matched: int | None = None
	num_tokens_dropped: int | None = None
	score: str | None = None
	tokens_matched: int | None = None
	typo_prefix_score: int | None = None
