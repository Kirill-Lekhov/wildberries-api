from wb_api.base.sync_api_mixin import SyncAPIMixin
from wb_api.base.dataclass import PingResponse, File
from wb_api.exception import FileModerationError, APIError
from wb_api.chat.base_api import BaseChatAPI
from wb_api.chat.dataclass import (
	ChatListResponse, ChatEventListRequest, ChatEventListResponse, FileDownloadRequest, ChatMessageCreateRequest,
	ChatMessageCreateResponse,
)

from typing import Optional


class SyncChatAPI(SyncAPIMixin, BaseChatAPI):
	def ping(self) -> PingResponse:
		url = self.router.ping()
		response = self.session.get(url)
		self.validate_response(response)
		return PingResponse.model_validate_json(response.text)

	def get_chat_list(self) -> ChatListResponse:
		url = self.router.chat_list()
		response = self.session.get(url)
		self.validate_response(response)
		return ChatListResponse.model_validate_json(response.text)

	def get_chat_event_list(self, request: Optional[ChatEventListRequest] = None) -> ChatEventListResponse:
		request = request or ChatEventListRequest()
		url = self.router.chat_event_list()
		response = self.session.get(url, params=request.as_request_params())
		self.validate_response(response)

		return ChatEventListResponse.model_validate_json(response.text)

	def download_file(self, request: FileDownloadRequest) -> File:
		url = self.router.file_download(request.download_id)
		response = self.session.get(url)

		if response.status_code == 202:
			raise FileModerationError()
		elif response.status_code == 200:
			if isinstance(response.content, bytes):
				return File.build(
					content=response.content,
					content_type=response.headers.get("Content-Type", ""),
					content_disposition=response.headers.get("Content-Disposition", ""),
				)
			else:
				raise APIError("Unknown response content type")

		self.validate_response(response)
		raise APIError("Unexpected file download error")

	def create_chat_message(self, request: ChatMessageCreateRequest) -> ChatMessageCreateResponse:
		url = self.router.chat_message_create()
		response = self.session.post(
			url,
			data=request.as_request_data(),
			files=[(i[0], i[1].content) for i in request.as_request_files()],
		)
		self.validate_response(response)
		return ChatMessageCreateResponse.model_validate_json(response.text)
