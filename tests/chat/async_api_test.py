from tests.fake_async_session import FakeAsyncSession
from wb_api.chat.async_api import AsyncChatAPI
from wb_api.chat.dataclass import ChatEventListRequest, FileDownloadRequest, ChatMessageCreateRequest
from wb_api.base.async_config import AsyncConfig
from wb_api.base.dataclass import File
from wb_api.const import BaseURL
from wb_api.exception import FileModerationError, APIError

from unittest.mock import patch, Mock, AsyncMock

import pytest
from aiohttp.formdata import FormData


def noop(*args, **kwargs) -> None:
	return None


class TestAsyncChatAPI:
	@pytest.mark.asyncio()
	async def test_ping(self):
		session = FakeAsyncSession("RAW DATA")
		config = AsyncConfig(session, BaseURL)		# type: ignore - for testing purposes
		api = AsyncChatAPI(config)

		with patch("wb_api.chat.async_api.PingResponse") as PingResponseMock:
			PingResponseMock.model_validate_json = Mock()
			PingResponseMock.model_validate_json.return_value = "DESERIALIZED DATA"

			with patch.object(api, "validate_response") as validate_response_mock:
				assert await api.ping() == "DESERIALIZED DATA"
				PingResponseMock.model_validate_json.assert_called_once_with("RAW DATA")
				validate_response_mock.assert_called_once_with(session.response)
				assert session.last_call_method == "GET"
				assert session.last_call_url == "https://buyer-chat-api.wildberries.ru/ping"
				assert session.last_call_params is None

	@pytest.mark.asyncio()
	async def test_get_chat_list(self):
		session = FakeAsyncSession("RAW DATA")
		config = AsyncConfig(session, BaseURL)		# type: ignore - for testing purposes
		api = AsyncChatAPI(config)

		with patch("wb_api.chat.async_api.ChatListResponse") as ChatListResponseMock:
			ChatListResponseMock.model_validate_json = Mock()
			ChatListResponseMock.model_validate_json.return_value = "DESERIALIZED DATA"

			with patch.object(api, "validate_response") as validate_response_mock:
				assert await api.get_chat_list() == "DESERIALIZED DATA"
				ChatListResponseMock.model_validate_json.assert_called_once_with("RAW DATA")
				validate_response_mock.assert_called_once_with(session.response)
				assert session.last_call_method == "GET"
				assert session.last_call_url == "https://buyer-chat-api.wildberries.ru/api/v1/seller/chats"
				assert session.last_call_params is None

	@pytest.mark.asyncio()
	async def test_get_chat_event_list(self):
		session = FakeAsyncSession("RAW DATA")
		config = AsyncConfig(session, BaseURL)		# type: ignore - for testing purposes
		api = AsyncChatAPI(config)
		request = ChatEventListRequest(next=512)

		with patch("wb_api.chat.async_api.ChatEventListResponse") as ChatEventListResponseMock:
			ChatEventListResponseMock.model_validate_json = Mock()
			ChatEventListResponseMock.model_validate_json.return_value = "DESERIALIZED DATA"

			with patch.object(api, "validate_response") as validate_response_mock:
				assert await api.get_chat_event_list() == "DESERIALIZED DATA"
				ChatEventListResponseMock.model_validate_json.assert_called_once_with("RAW DATA")
				validate_response_mock.assert_called_once_with(session.response)
				assert session.last_call_method == "GET"
				assert session.last_call_url == "https://buyer-chat-api.wildberries.ru/api/v1/seller/events"
				assert session.last_call_params == {}

				ChatEventListResponseMock.reset_mock()
				validate_response_mock.reset_mock()
				assert await api.get_chat_event_list(request) == "DESERIALIZED DATA"
				ChatEventListResponseMock.model_validate_json.assert_called_once_with("RAW DATA")
				validate_response_mock.assert_called_once_with(session.response)
				assert session.last_call_method == "GET"
				assert session.last_call_url == "https://buyer-chat-api.wildberries.ru/api/v1/seller/events"
				assert session.last_call_params == {"next": 512}

	@pytest.mark.asyncio()
	async def test_download_file(self):
		session = Mock()
		session.get.return_value = AsyncMock()
		session.get.return_value.__aenter__.return_value = AsyncMock()
		session.get.return_value.__aenter__.return_value.status = 202
		session.get.return_value.__aexit__.return_value = None
		config = AsyncConfig(session, BaseURL)
		api = AsyncChatAPI(config)
		request = FileDownloadRequest(download_id="1")

		with pytest.raises(FileModerationError):
			await api.download_file(request)

		session.get.reset_mock()
		session.get.return_value.__aenter__.return_value.status = 200
		session.get.return_value.__aenter__.return_value.content.read = AsyncMock()
		session.get.return_value.__aenter__.return_value.content.read.return_value = b"RAW DATA"
		session.get.return_value.__aenter__.return_value.headers = {
			"Content-Type": "text/plain",
			"Content-Length": "8",
			"Content-Disposition": "attachment; filename=0e1926ce-6563-4e69-a80c-737553419531.txt"
		}
		file = await api.download_file(request)
		assert isinstance(file, File)
		assert file.content.read() == b"RAW DATA"
		assert file.content_type == "text/plain"
		assert file.content_length == 8
		assert file.name == "0e1926ce-6563-4e69-a80c-737553419531.txt"
		session.get.assert_called_once_with("https://buyer-chat-api.wildberries.ru/api/v1/seller/download/1")
		session.get.return_value.__aenter__.return_value.status = 400

		with pytest.raises(APIError, match="Unexpected file download error"):
			with patch.object(api, "validate_response", new=noop):
				await api.download_file(request)

	@pytest.mark.asyncio()
	async def test_create_chat_message(self):
		session = Mock()
		session.post.return_value = AsyncMock()
		session.post.return_value.__aenter__.return_value = AsyncMock()
		session.post.return_value.__aenter__.return_value.status = 200
		session.post.return_value.__aenter__.return_value.text.return_value = "RAW DATA"
		session.post.return_value.__aexit__.return_value = None
		config = AsyncConfig(session, BaseURL)
		api = AsyncChatAPI(config)
		request = ChatMessageCreateRequest(reply_sign="REPLY_SIGN", message="MESSAGE")

		with patch("wb_api.chat.async_api.ChatMessageCreateResponse") as ChatMessageCreateResponseMock:
			ChatMessageCreateResponseMock.model_validate_json.return_value = "DESERIALIZED DATA"

			with patch.object(api, "validate_response") as validate_response_mock:
				assert await api.create_chat_message(request) == "DESERIALIZED DATA"
				ChatMessageCreateResponseMock.model_validate_json.assert_called_once_with("RAW DATA")
				validate_response_mock.assert_called_once_with(session.post.return_value.__aenter__.return_value)
				session.post.assert_called_once()
				assert session.post.call_args_list[0].args[0] == (
					"https://buyer-chat-api.wildberries.ru/api/v1/seller/message"
				)
				form_data = session.post.call_args_list[0].kwargs["data"]
				assert isinstance(form_data, FormData)
				assert len(form_data._fields) == 2
				assert form_data._fields[0][0]["name"] == "replySign"
				assert form_data._fields[0][2] == "REPLY_SIGN"
				assert form_data._fields[1][0]["name"] == "message"
				assert form_data._fields[1][2] == "MESSAGE"

		session.post.reset_mock()
		request = ChatMessageCreateRequest(
			reply_sign="REPLY_SIGN",
			file=[File.build(b"deadbee", content_type="text/plain", name="text.txt")],
		)

		with patch("wb_api.chat.async_api.ChatMessageCreateResponse") as ChatMessageCreateResponseMock:
			ChatMessageCreateResponseMock.model_validate_json.return_value = "DESERIALIZED DATA"

			with patch.object(api, "validate_response") as validate_response_mock:
				assert await api.create_chat_message(request) == "DESERIALIZED DATA"
				ChatMessageCreateResponseMock.model_validate_json.assert_called_once_with("RAW DATA")
				validate_response_mock.assert_called_once_with(session.post.return_value.__aenter__.return_value)
				session.post.assert_called_once()
				assert session.post.call_args_list[0].args[0] == (
					"https://buyer-chat-api.wildberries.ru/api/v1/seller/message"
				)
				form_data = session.post.call_args_list[0].kwargs["data"]
				assert isinstance(form_data, FormData)
				assert len(form_data._fields) == 2
				assert form_data._fields[0][0]["name"] == "replySign"
				assert form_data._fields[0][2] == "REPLY_SIGN"
				assert form_data._fields[1][0]["name"] == "file"
				assert form_data._fields[1][0]["filename"] == "text.txt"
				assert form_data._fields[1][1] == {"Content-Type": "text/plain"}
				assert form_data._fields[1][2].read() == b"deadbee"
