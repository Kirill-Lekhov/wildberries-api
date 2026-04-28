from wb_api.chat.sync_api import SyncChatAPI
from wb_api.chat.dataclass import ChatEventListRequest, FileDownloadRequest, ChatMessageCreateRequest
from wb_api.base.sync_config import SyncConfig
from wb_api.base.dataclass.file import File
from wb_api.const import BaseURL
from wb_api.exception import FileModerationError, APIError

from unittest.mock import Mock, patch

import pytest


def noop(*args, **kwargs) -> None:
	return None


class TestSyncChatAPI:
	def test_ping(self):
		session = Mock()
		session.get = Mock()
		session.get.return_value = Mock()
		session.get.return_value.text = "RAW DATA"
		config = SyncConfig(session, BaseURL)
		api = SyncChatAPI(config)

		with patch("wb_api.chat.sync_api.PingResponse") as PingResponseMock:
			PingResponseMock.model_validate_json = Mock()
			PingResponseMock.model_validate_json.return_value = "DESERIALIZED DATA"

			with patch.object(api, "validate_response") as validate_response_mock:
				assert api.ping() == "DESERIALIZED DATA"
				PingResponseMock.model_validate_json.assert_called_once_with("RAW DATA")
				validate_response_mock.assert_called_once_with(session.get.return_value)
				session.get.assert_called_once_with("https://buyer-chat-api.wildberries.ru/ping")

	def test_get_chat_list(self):
		session = Mock()
		session.get = Mock()
		session.get.return_value = Mock()
		session.get.return_value.text = "RAW DATA"
		config = SyncConfig(session, BaseURL)
		api = SyncChatAPI(config)

		with patch("wb_api.chat.sync_api.ChatListResponse") as ChatListResponseMock:
			ChatListResponseMock.model_validate_json = Mock()
			ChatListResponseMock.model_validate_json.return_value = "DESERIALIZED DATA"

			with patch.object(api, "validate_response") as validate_response_mock:
				assert api.get_chat_list() == "DESERIALIZED DATA"
				ChatListResponseMock.model_validate_json.assert_called_once_with("RAW DATA")
				validate_response_mock.assert_called_once_with(session.get.return_value)
				session.get.assert_called_once_with("https://buyer-chat-api.wildberries.ru/api/v1/seller/chats")

	def test_get_chat_event_list(self):
		session = Mock()
		session.get = Mock()
		session.get.return_value = Mock()
		session.get.return_value.text = "RAW DATA"
		config = SyncConfig(session, BaseURL)
		api = SyncChatAPI(config)
		request = ChatEventListRequest(next=512)

		with patch("wb_api.chat.sync_api.ChatEventListResponse") as ChatEventListResponseMock:
			ChatEventListResponseMock.model_validate_json = Mock()
			ChatEventListResponseMock.model_validate_json.return_value = "DESERIALIZED DATA"

			with patch.object(api, "validate_response") as validate_response_mock:
				assert api.get_chat_event_list() == "DESERIALIZED DATA"
				ChatEventListResponseMock.model_validate_json.assert_called_once_with("RAW DATA")
				validate_response_mock.assert_called_once_with(session.get.return_value)
				session.get.assert_called_once_with(
					"https://buyer-chat-api.wildberries.ru/api/v1/seller/events",
					params={},
				)

				ChatEventListResponseMock.model_validate_json.reset_mock()
				validate_response_mock.reset_mock()
				session.get.reset_mock()
				assert api.get_chat_event_list(request) == "DESERIALIZED DATA"
				ChatEventListResponseMock.model_validate_json.assert_called_once_with("RAW DATA")
				validate_response_mock.assert_called_once_with(session.get.return_value)
				session.get.assert_called_once_with(
					"https://buyer-chat-api.wildberries.ru/api/v1/seller/events",
					params={"next": 512},
				)

	def test_download_file(self):
		session = Mock()
		session.get = Mock()
		session.get.return_value = Mock()
		session.get.return_value.status_code = 202
		session.get.return_value.content = b"RAW DATA"
		session.get.return_value.headers = {
			"Content-Type": "text/plain",
			"Content-Length": "8",
			"Content-Disposition": "attachment; filename=0e1926ce-6563-4e69-a80c-737553419531.txt"
		}
		config = SyncConfig(session, BaseURL)
		api = SyncChatAPI(config)
		request = FileDownloadRequest(download_id="1")

		with pytest.raises(FileModerationError):
			assert api.download_file(request)

		session.get.reset_mock()
		session.get.return_value.status_code = 200
		file = api.download_file(request)
		assert isinstance(file, File)
		assert file.content.read() == b"RAW DATA"
		assert file.name == "0e1926ce-6563-4e69-a80c-737553419531.txt"
		assert file.content_length == 8
		assert file.content_type == "text/plain"
		session.get.assert_called_once_with("https://buyer-chat-api.wildberries.ru/api/v1/seller/download/1")

		session.get.reset_mock()
		session.get.return_value.content = "RAW DATA"

		with pytest.raises(APIError, match="Unknown response content type"):
			assert api.download_file(request)

		session.get.return_value.status_code = 400

		with pytest.raises(APIError, match="Unexpected file download error"):
			with patch.object(api, "validate_response", new=noop):
				api.download_file(request)

	def test_create_chat_message(self):
		session = Mock()
		session.post = Mock()
		session.post.return_value = Mock()
		session.post.return_value.text = "RAW DATA"
		config = SyncConfig(session, BaseURL)
		api = SyncChatAPI(config)
		request = ChatMessageCreateRequest(reply_sign="REPLY_SIGN", message="MESSAGE")

		with patch("wb_api.chat.sync_api.ChatMessageCreateResponse") as ChatMessageCreateResponseMock:
			ChatMessageCreateResponseMock.model_validate_json = Mock()
			ChatMessageCreateResponseMock.model_validate_json.return_value = "DESERIALIZED DATA"

			with patch.object(api, "validate_response") as validate_response_mock:
				assert api.create_chat_message(request) == "DESERIALIZED DATA"
				ChatMessageCreateResponseMock.model_validate_json.assert_called_once_with("RAW DATA")
				validate_response_mock.assert_called_once_with(session.post.return_value)
				session.post.assert_called_once_with(
					"https://buyer-chat-api.wildberries.ru/api/v1/seller/message",
					data={
						"replySign": "REPLY_SIGN",
						"message": "MESSAGE",
					},
					files=[],
				)

		request = ChatMessageCreateRequest(
			reply_sign="REPLY_SIGN",
			file=[File.build(b"deadbee", "text/plain", 7, name="text.txt")],
		)
		ChatMessageCreateResponseMock.reset_mock()
		validate_response_mock.reset_mock()
		session.post.reset_mock()

		with patch("wb_api.chat.sync_api.ChatMessageCreateResponse") as ChatMessageCreateResponseMock:
			ChatMessageCreateResponseMock.model_validate_json = Mock()
			ChatMessageCreateResponseMock.model_validate_json.return_value = "DESERIALIZED DATA"

			with patch.object(api, "validate_response") as validate_response_mock:
				assert api.create_chat_message(request) == "DESERIALIZED DATA"
				ChatMessageCreateResponseMock.model_validate_json.assert_called_once_with("RAW DATA")
				validate_response_mock.assert_called_once_with(session.post.return_value)
				assert session.post.call_args_list[0].args[0] == (
					"https://buyer-chat-api.wildberries.ru/api/v1/seller/message"
				)
				assert session.post.call_args_list[0].kwargs["data"] == {
					"replySign": "REPLY_SIGN",
				}
				assert len(session.post.call_args_list[0].kwargs["files"]) == 1
				assert session.post.call_args_list[0].kwargs["files"][0][0] == "file"
				assert session.post.call_args_list[0].kwargs["files"][0][1].read() == b"deadbee"
