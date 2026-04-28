from wb_api.chat.dataclass.good_card import GoodCard

import arrow


class TestGoodCard:
	def test_validate_datetime(self):
		assert GoodCard.validate_datetime("2026-04-21T00:00:00Z") == arrow.get(2026, 4, 21)
