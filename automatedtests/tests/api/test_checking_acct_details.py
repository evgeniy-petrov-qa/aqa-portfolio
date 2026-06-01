import pytest
from automatedtests.pages.api.api_registry import api_registry
from automatedtests.pages.api.http_client import API


@pytest.mark.api
class TestCheckingAcctDetails:
    @pytest.mark.smoke
    def test_checking_acct_details(self, urls):
        api=API()
        registry_key = 'checking_contact:get'
        api.make_request(
            url=urls.firstplaidypusbank + api_registry[registry_key]['endpoint'],
            registry_key=registry_key
        )

