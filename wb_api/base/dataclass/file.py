import re
from io import BufferedReader, BytesIO
from typing import ClassVar, Optional, overload

from pydantic.main import BaseModel
from pydantic.config import ConfigDict
from pydantic.fields import Field


class File(BaseModel):
	model_config = ConfigDict(arbitrary_types_allowed=True)

	RE_FILENAME: ClassVar[re.Pattern] = re.compile(
		r"[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}\.[a-zA-Z]+",
	)

	name: str
	content: BufferedReader
	content_type: str
	content_length: int = Field(ge=1, le=5_000_000)

	@overload
	@classmethod
	def build(cls, content: bytes, content_type: str, *, name: str) -> "File": ...
	@overload
	@classmethod
	def build(cls, content: bytes, content_type: str, *, content_disposition: str) -> "File": ...
	@classmethod
	def build(
		cls,
		content: bytes,
		content_type: str,
		*,
		name: Optional[str] = None,
		content_disposition: Optional[str] = None,
	) -> "File":
		filename = "file"

		if name:
			filename = name
		elif content_disposition:
			if result := cls.RE_FILENAME.search(content_disposition):
				filename = result.group()

		return cls(
			name=filename,
			content=BufferedReader(BytesIO(content)),
			content_type=content_type,
			content_length=len(content),
		)
