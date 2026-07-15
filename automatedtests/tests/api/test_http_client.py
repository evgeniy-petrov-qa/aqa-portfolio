import pytest

from automatedtests.pages.api.http_client import API, HttpMethod


@pytest.mark.api
class TestAPIClient:

    def test_raises_on_unexpected_status_code(self, mocker):
        api = API()
        mock_get = mocker.patch.object(api.session, "get")
        mock_get.return_value.status_code = 404

        with pytest.raises(AssertionError, match="404"):
            api.make_request(
                url="https://example.com",
                method=HttpMethod.GET,
                validate_response=False,
            )
