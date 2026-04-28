from wb_api.chat.dataclass.chat_event_list import Request, File, Image, Event, Result
from wb_api.chat.const import EventType, MessageSender

import arrow


class TestRequest:
	def test_as_request_params(self):
		request = Request()
		assert request.as_request_params() == {}

		request = Request(next=512)
		assert request.as_request_params() == {"next": 512}


class TestFile:
	def test_validate_date(self):
		assert File.validate_date("2026-04-21T00:00:00Z") == arrow.get(2026, 4, 21)


class TestImage:
	def test_validate_date(self):
		assert Image.validate_date("2026-04-21T00:00:00Z") == arrow.get(2026, 4, 21)


class TestEvent:
	def test_created_at(self):
		event = Event.model_validate({
			"chatID": "CHAT_ID",
			"eventID": "EVENT_ID",
			"eventType": EventType.MESSAGE,
			"addTimestamp": 1776729600,
			"addTime": "00:00:00",
			"sender": MessageSender.CLIENT,
		})
		assert event.created_at == arrow.get(2026, 4, 21)


class TestResult:
	def test_validate_datetime(self):
		assert Result.validate_datetime("2026-04-21T00:00:00Z") == arrow.get(2026, 4, 21)
