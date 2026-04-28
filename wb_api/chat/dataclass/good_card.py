from typing import Any

import arrow
from pydantic.main import BaseModel
from pydantic.fields import Field
from pydantic.config import ConfigDict
from pydantic.functional_validators import field_validator


class GoodCard(BaseModel):
	model_config = ConfigDict(arbitrary_types_allowed=True)

	date: arrow.Arrow
	sku: int = Field(validation_alias="nmID")
	price: int
	price_currency: str = Field(validation_alias="priceCurrency")
	rid: str
	size: str

	@field_validator("date", mode="before")
	@classmethod
	def validate_datetime(cls, value: Any) -> arrow.Arrow:
		return arrow.get(value)
