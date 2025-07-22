from enum import Enum
from typing import Final


class BaseURL:
	COMMON: Final[str] = "https://common-api.wildberries.ru"
	FEEDBACK: Final[str] = "https://feedbacks-api.wildberries.ru"


class Header(Enum):
	AUTHORIZATION = "Authorization"
	LOCALE = "X-Locale"
