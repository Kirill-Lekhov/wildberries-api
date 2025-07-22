from wb_api.base.sync_api_mixin import SyncAPIMixin
from wb_api.exception import InvalidResponseError, AuthorizationError, NotFoundError

from unittest.mock import Mock
from http import HTTPStatus
from typing import Optional, Type

import pytest
from requests.sessions import Session


class TestSyncAPIMixin:
	@pytest.mark.asyncio()
	@pytest.mark.parametrize(
		"status, expected_error_type, expected_error_text",
		[
			(HTTPStatus.OK, None, None),
			(HTTPStatus.FORBIDDEN, None, None),
			(HTTPStatus.FORBIDDEN, AuthorizationError, "Unauthorized"),
			(HTTPStatus.UNAUTHORIZED, AuthorizationError, "Unauthorized"),
			(HTTPStatus.NOT_FOUND, NotFoundError, "Resource was not found"),
			(HTTPStatus.INTERNAL_SERVER_ERROR, InvalidResponseError, "Response is not valid"),
		],
	)
	async def test_validate_response(
		self,
		status: HTTPStatus,
		expected_error_type: Optional[Type[Exception]],
		expected_error_text: Optional[str],
	):
		session = Session()
		api = SyncAPIMixin(session)
		response = Mock()
		response.status_code = status

		if expected_error_type is None:
			assert api.validate_response(response, status) is None
		else:
			with pytest.raises(expected_error_type, match=expected_error_text):
				api.validate_response(response)
