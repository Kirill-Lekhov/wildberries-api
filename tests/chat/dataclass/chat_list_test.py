from wb_api.chat.dataclass.chat_list import LastMessage

import arrow


class TestLastMessage:
	def test_validate_datetime(self):
		assert LastMessage.validate_datetime("2026-04-21T00:00:00Z") == arrow.get(2026, 4, 21)
