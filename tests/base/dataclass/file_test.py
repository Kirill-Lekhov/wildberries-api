from wb_api.base.dataclass.file import File


class TestFile:
	def test_build(self):
		file = File.build(
			content=b"deadbee",
			content_type="application/octet-stream",
			name="",
		)
		assert file.name == "file"

		file = File.build(
			content=b"deadbee",
			content_type="application/octet-stream",
			content_disposition="",
		)
		assert file.name == "file"

		file = File.build(
			content=b"deadbee",
			content_type="application/octet-stream",
			content_disposition="attachment; filename=image.png",
		)
		assert file.name == "file"

		file = File.build(
			content=b"deadbee",
			content_type="application/octet-stream",
			name="filename",
		)
		assert file.name == "filename"

		file = File.build(
			content=b"deadbee",
			content_type="application/octet-stream",
			content_disposition="filename=b7f19c71-1da6-44d5-b608-2a4e77999cf0.png",
		)
		assert file.name == "b7f19c71-1da6-44d5-b608-2a4e77999cf0.png"

		file = File.build(
			content=b"deadbee",
			content_type="application/octet-stream",
			content_disposition="attachment; filename=b7f19c71-1da6-44d5-b608-2a4e77999cf0.png",
		)
		assert file.name == "b7f19c71-1da6-44d5-b608-2a4e77999cf0.png"
