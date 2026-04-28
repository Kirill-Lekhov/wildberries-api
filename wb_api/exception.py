class APIError(Exception):
	pass


class InvalidResponseError(APIError):
	pass


class AuthorizationError(InvalidResponseError):
	pass


class NotFoundError(InvalidResponseError):
	pass


class FileModerationError(InvalidResponseError):
	pass
