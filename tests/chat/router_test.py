from wb_api.chat.router import ChatRouter


class TestChatRouter:
	def test_ping(self):
		router = ChatRouter("")
		assert router.ping() == "/ping"

	def test_chat_list(self):
		router = ChatRouter("")
		assert router.chat_list() == "/api/v1/seller/chats"

	def test_chat_event_list(self):
		router = ChatRouter("")
		assert router.chat_event_list() == "/api/v1/seller/events"

	def test_chat_message_create(self):
		router = ChatRouter("")
		assert router.chat_message_create() == "/api/v1/seller/message"

	def test_file_download(self):
		router = ChatRouter("")
		assert router.file_download("") == "/api/v1/seller/download/"
		assert router.file_download("12316276192") == "/api/v1/seller/download/12316276192"
