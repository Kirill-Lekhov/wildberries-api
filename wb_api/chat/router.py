from wb_api.base.router import Router
from wb_api.generic.functools import cache


class ChatRouter(Router):
	@cache
	def ping(self):
		return f"{self.base_url}/ping"

	@cache
	def chat_list(self) -> str:
		return f"{self.base_url}/api/v1/seller/chats"

	@cache
	def chat_event_list(self) -> str:
		return f"{self.base_url}/api/v1/seller/events"

	@cache
	def chat_message_create(self) -> str:
		return f"{self.base_url}/api/v1/seller/message"

	def file_download(self, download_id: str) -> str:
		return f"{self.base_url}/api/v1/seller/download/{download_id}"
