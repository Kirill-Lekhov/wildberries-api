from pydantic.main import BaseModel


class Request(BaseModel):
	download_id: str
