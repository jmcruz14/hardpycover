from typing import Literal
from datetime import datetime, date
from pydantic import BaseModel, Field
from .utils import CachedImage


# NOTE: expand the User class accordingly
class User(BaseModel):
	user_id: int | None = Field(default=None, alias="id")
	bio: str | None = None
	cached_image: CachedImage | None = None
	birthdate: str | None = None
	books_count: int | None = None
	created_at: datetime | None = None
	email: str | None = None
	followers_count: int | None = None
	followed_users_count: int | None = None
	image_id: int | None = None
	last_activity_at: datetime | None = None
	last_sign_in_at: datetime | None = None
	librarian_roles: list[str] | None = (
		None  # literal but which values? (appender, editor, librarian)
	)
	object_type: Literal["User"] | None = None
	username: str | None = None
	updated_at: datetime | None = None


class UserStatus(BaseModel):
	user_status_id: int | None = Field(default=None, alias="id")
	status: Literal["created", "activated", "banned"] | None = None


class Me(BaseModel):
	me_id: int | None = Field(default=None, alias="id")
	access_level: int | None = None
	account_privacy_setting_id: int | None = None
	activity_privacy_settings_id: int | None = None
	admin: bool | None = False
	bio: str | None = None
	birthdate: str | date | None = None
	books_count: int | None = None
	cached_cover: CachedImage | None = None
	cached_image: CachedImage | None = None
	confirmed_at: datetime | None = None
	confirmation_sent_at: datetime | None = None
	created_at: datetime | None = None
	current_sign_in_at: datetime | None = None
	default_reading_format_id: int | None = None
	email: str | None = None
	email_verified: bool | None = None
	followers_count: int | None = None
	followed_users_count: int | None = None
	image_id: int | None = None
	last_activity_at: datetime | None = None
	last_sign_in_at: datetime | None = None
	librarian_roles: list[str] | None = (
		None  # literal but which values? (appender, editor, librarian)
	)
	location: str | None = None
	object_type: Literal["User"] | None = None
	username: str | None = None
	updated_at: datetime | None = None
	timezone: str | None = None
	status_id: int | None = None
	sign_in_count: int | None = None
	referrer_url: str | None = None
	pronoun_possessive: str | None = None
	pronoun_personal: str | None = None
