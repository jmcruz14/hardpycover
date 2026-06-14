from datetime import datetime
from pydantic import BaseModel
from typing_extensions import TypedDict

class NotificationChannels(TypedDict):
  channel: str
  id: int

class NotifierUser(TypedDict):
  name: str
  username: str

class NotificationDelivery(TypedDict):
  channel_id: int
  id: int
  notification_id: int
  read: bool
  read_at: datetime
  sent_at: datetime
  user_id: int

class Notification(BaseModel):
  created_at: datetime | None = None
  description: str | None = None
  link: str | None = None
  id: int | None = None
  link_text: str | None = None
  notifier_user_id: int | None = None
  priority: int | None = None
  title: str | None = None
  uid: str | None = None
  notification_type_id: int | None = None
  notifierUser: NotifierUser | None = None
  notification_deliveries: list[NotificationDelivery] | None = None