from wb_api.base.dataclass import File

from typing import Optional, List, Dict, Any, ClassVar, Tuple, overload
from functools import reduce
from operator import add

import arrow
from pydantic.main import BaseModel
from pydantic.fields import Field
from pydantic.functional_validators import model_validator
from pydantic.config import ConfigDict


class Request(BaseModel):
	model_config = ConfigDict(frozen=True)

	MAX_PAYLOAD_SIZE: ClassVar[int] = 30_000_000		# Max sum of file size: 30 Mb (not MiB)

	reply_sign: str = Field(min_length=1, max_length=255, serialization_alias="replySign")
	message: Optional[str] = Field(min_length=1, max_length=1000)
	file: Optional[List[File]] = None

	@overload
	def __init__(self, *, reply_sign: str, message: str) -> None: ...
	@overload
	def __init__(self, *, reply_sign: str, file: List[File]) -> None: ...
	def __init__(self, *, reply_sign: str, message: Optional[str] = None, file: Optional[List[File]] = None) -> None:
		super().__init__(reply_sign=reply_sign, message=message, file=file)

	@model_validator(mode="after")
	def validate_payload(self) -> "Request":
		if self.message is None and self.file is None:
			raise ValueError("Message or file must be specified")

		if self.file and reduce(add, (i.content_length for i in self.file), 0) > self.MAX_PAYLOAD_SIZE:
			raise ValueError("The maximum file size has been exceeded")

		return self

	def as_request_data(self) -> Dict[str, Any]:
		return self.model_dump(include={"reply_sign", "message"}, exclude_none=True, by_alias=True)

	def as_request_files(self) -> List[Tuple[str, File]]:
		if self.file is None:
			return []

		return [("file", file) for file in self.file]


class Result(BaseModel):
	add_time: int = Field(validation_alias="addTime")
	chat_id: str = Field(validation_alias="chatID")
	sign: str

	@property
	def created_at(self) -> arrow.Arrow:
		return arrow.get(self.add_time)


class Response(BaseModel):
	result: Result
	errors: Optional[List[str]] = None
