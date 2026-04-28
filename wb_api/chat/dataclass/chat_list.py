from wb_api.chat.dataclass.good_card import GoodCard

from typing import List, Optional, Any

import arrow
from pydantic.main import BaseModel
from pydantic.fields import Field
from pydantic.config import ConfigDict
from pydantic.functional_validators import field_validator


class LastMessage(BaseModel):
	model_config = ConfigDict(arbitrary_types_allowed=True)

	text: str
	created_at: arrow.Arrow = Field(validation_alias="addTimestamp")

	@field_validator("created_at", mode="before")
	@classmethod
	def validate_datetime(cls, value: Any) -> arrow.Arrow:
		return arrow.get(value)


class Chat(BaseModel):
	id: str = Field(validation_alias="chatID")
	reply_sign: str = Field(validation_alias="replySign")
	client_name: str = Field(validation_alias="clientName")
	good_card: GoodCard = Field(validation_alias="goodCard")
	last_message: Optional[LastMessage] = Field(default=None, validation_alias="lastMessage")


class Response(BaseModel):
	result: List[Chat] = Field(default_factory=list)
	errors: Optional[List[str]] = None
