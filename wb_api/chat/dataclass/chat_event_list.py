from wb_api.base.dataclass import BaseRequest
from wb_api.chat.dataclass.good_card import GoodCard
from wb_api.chat.const import EventType, MessageSource, MessageSender

from typing import Optional, List, Any

import arrow
from pydantic.main import BaseModel
from pydantic.fields import Field
from pydantic.functional_validators import field_validator
from pydantic.config import ConfigDict


class Request(BaseRequest):
	next: Optional[int] = None

	def as_request_params(self):
		return self.model_dump(include={"next"}, exclude_none=True)


class File(BaseModel):
	model_config = ConfigDict(arbitrary_types_allowed=True)

	content_type: str = Field(validation_alias="contentType")
	date: arrow.Arrow
	download_id: Optional[str] = Field(default=None, validation_alias="downloadID")
	name: str
	url: Optional[str] = None
	size: int		# in bytes

	@field_validator("date", mode="before")
	@classmethod
	def validate_date(cls, value: Any) -> arrow.Arrow:
		return arrow.get(value)


class Image(BaseModel):
	model_config = ConfigDict(arbitrary_types_allowed=True)

	date: arrow.Arrow
	download_id: Optional[str] = Field(default=None, validation_alias="downloadID")
	url: Optional[str] = None

	@field_validator("date", mode="before")
	@classmethod
	def validate_date(cls, value: Any) -> arrow.Arrow:
		return arrow.get(value)


class Attachments(BaseModel):
	good_card: Optional[GoodCard] = Field(default=None, validation_alias="goodCard")
	files: List[File] = Field(default_factory=list)
	images: List[Image] = Field(default_factory=list)


class Message(BaseModel):
	attachments: Optional[Attachments] = None
	text: str = ""


class Event(BaseModel):
	chat_id: str = Field(validation_alias="chatID")
	event_id: str = Field(validation_alias="eventID")
	event_type: EventType = Field(validation_alias="eventType")
	add_timestamp: int = Field(validation_alias="addTimestamp")
	add_time: str = Field(validation_alias="addTime")
	sender: MessageSender
	# optional attrs
	is_new_chat: Optional[bool] = Field(default=None, validation_alias="isNewChat")
	message: Optional[Message] = None
	source: Optional[MessageSource] = None
	reply_sign: Optional[str] = Field(default=None, validation_alias="replySign")
	client_name: Optional[str] = Field(default=None, validation_alias="clientName")

	@property
	def created_at(self) -> arrow.Arrow:
		return arrow.get(self.add_timestamp)


class Result(BaseModel):
	model_config = ConfigDict(arbitrary_types_allowed=True)

	next: int
	newest_event_time: Optional[arrow.Arrow] = Field(default=None, validation_alias="newestEventTime")
	oldest_event_time: Optional[arrow.Arrow] = Field(default=None, validation_alias="oldestEventTime")
	total_events: int = Field(validation_alias="totalEvents")
	events: List[Event]

	@field_validator("newest_event_time", "oldest_event_time", mode="before")
	@classmethod
	def validate_datetime(cls, value: Any) -> Optional[arrow.Arrow]:
		if value is None:
			return None

		return arrow.get(value)


class Response(BaseModel):
	result: Result
	errors: Optional[List[str]]
