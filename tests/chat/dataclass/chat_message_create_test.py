from wb_api.chat.dataclass.chat_message_create import Request, Result
from wb_api.base.dataclass import File

import arrow
import pytest
from pydantic_core import ValidationError


class TestRequest:
	def test___init__(self):
		request = Request(reply_sign="REPLY_SIGN", message="MESSAGE")
		assert request.reply_sign == "REPLY_SIGN"
		assert request.message == "MESSAGE"
		assert request.file is None

		request = Request(
			reply_sign="REPLY_SIGN",
			file=[File.build(b"test", content_type="text/plain", name="test.txt")],
		)
		assert request.reply_sign == "REPLY_SIGN"
		assert request.message is None
		assert isinstance(request.file, list)
		assert len(request.file) == 1
		assert request.file[0].name == "test.txt"

	def test_validate_payload(self):
		with pytest.raises(ValidationError, match="Message or file must be specified"):
			Request.model_validate({"reply_sign": "REPLY_SIGN"})

		with pytest.raises(ValidationError, match="The maximum file size has been exceeded"):
			Request.model_validate({
				"reply_sign": "REPLY_SIGN",
				"file": [
					File.build(b"0" * 5_000_000, content_type="text/plain", name="test.txt"),
					File.build(b"0" * 5_000_000, content_type="text/plain", name="test.txt"),
					File.build(b"0" * 5_000_000, content_type="text/plain", name="test.txt"),
					File.build(b"0" * 5_000_000, content_type="text/plain", name="test.txt"),
					File.build(b"0" * 5_000_000, content_type="text/plain", name="test.txt"),
					File.build(b"0" * 5_000_000, content_type="text/plain", name="test.txt"),
					File.build(b"0", content_type="text/plain", name="test.txt"),
				],
			})

	def test_as_request_data(self):
		request = Request(reply_sign="REPLY_SIGN", message="MESSAGE")
		assert request.as_request_data() == {
			"replySign": "REPLY_SIGN",
			"message": "MESSAGE"
		}

	def test_as_request_files(self):
		file = File.build(b"test", content_type="text/plain", name="test.txt")
		request = Request(
			reply_sign="REPLY_SIGN",
			message="MESSAGE",
		)
		request_files = request.as_request_files()
		assert len(request_files) == 0

		file = File.build(b"test", content_type="text/plain", name="test.txt")
		request = Request(
			reply_sign="REPLY_SIGN",
			file=[file],
		)
		request_files = request.as_request_files()
		assert len(request_files) == 1
		assert request_files[0][0] == "file"
		assert request_files[0][1] is file


class TestResult:
	def test_created_at(self):
		result = Result.model_validate({
			"addTime": 1776729600,
			"chatID": "CHAT_ID",
			"sign": "SIGN",
		})
		assert result.created_at == arrow.get(2026, 4, 21)
