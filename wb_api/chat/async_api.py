from wb_api.base.async_api_mixin import AsyncAPIMixin
from wb_api.base.dataclass import PingResponse, File
from wb_api.exception import FileModerationError, APIError
from wb_api.chat.base_api import BaseChatAPI
from wb_api.chat.dataclass import (
	ChatListResponse, ChatEventListRequest, ChatEventListResponse, FileDownloadRequest, ChatMessageCreateRequest,
	ChatMessageCreateResponse,
)

from typing import Optional

from aiohttp import FormData


class AsyncChatAPI(AsyncAPIMixin, BaseChatAPI):
	async def ping(self) -> PingResponse:
		url = self.router.ping()

		async with self.session.get(url) as response:
			self.validate_response(response)
			return PingResponse.model_validate_json(await response.text())

	async def get_chat_list(self) -> ChatListResponse:
		url = self.router.chat_list()

		async with self.session.get(url) as response:
			self.validate_response(response)
			return ChatListResponse.model_validate_json(await response.text())

	async def get_chat_event_list(self, request: Optional[ChatEventListRequest] = None) -> ChatEventListResponse:
		request = request or ChatEventListRequest()
		url = self.router.chat_event_list()

		async with self.session.get(url, params=request.as_request_params()) as response:
			self.validate_response(response)
			return ChatEventListResponse.model_validate_json(await response.text())

	async def download_file(self, request: FileDownloadRequest) -> File:
		url = self.router.file_download(request.download_id)

		async with self.session.get(url) as response:
			if response.status == 202:
				raise FileModerationError()
			elif response.status == 200:
				return File.build(
					content=await response.content.read(),
					content_type=response.headers.get("Content-Type", ""),
					content_disposition=response.headers.get("Content-Disposition", ""),
				)

			self.validate_response(response)
			raise APIError("Unexpected file download error")

	async def create_chat_message(self, request: ChatMessageCreateRequest) -> ChatMessageCreateResponse:
		url = self.router.chat_message_create()
		data = FormData()

		for field_name, field_value in request.as_request_data().items():
			data.add_field(field_name, field_value)

		for field_name, file in request.as_request_files():
			data.add_field(field_name, file.content, filename=file.name, content_type=file.content_type)

		async with self.session.post(url, data=data) as response:
			self.validate_response(response)
			return ChatMessageCreateResponse.model_validate_json(await response.text())
