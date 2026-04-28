from wb_api.base.config import BaseURL
from wb_api.chat.router import ChatRouter
from wb_api.base.api import API

from typing import Type


class BaseChatAPI(API[ChatRouter]):
	@staticmethod
	def make_router(base_url: Type[BaseURL]) -> ChatRouter:
		return ChatRouter(base_url=base_url.CHAT)
