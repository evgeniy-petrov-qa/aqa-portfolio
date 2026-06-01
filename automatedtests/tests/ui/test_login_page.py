import pytest
from playwright.sync_api import expect

from automatedtests.data.test_data import TestData


@pytest.mark.ui
class TestLoginPage:

    @pytest.mark.smoke
    def test_successful_login(
            self,
            login_page,
            login_page_blocks,
            study_tracker_page
    ) -> None:
        login_page.open_login_page()
        login_page_blocks.login_success()
        study_tracker_page.should_have_url(f"{login_page.urls.qa_playground}/study-tracker/dashboard")
        study_tracker_page.heading.should_be_visible()


    @pytest.mark.regression
    def test_login_with_wrong_email(self, login_page, login_page_blocks) -> None:
        login_page.open_login_page()
        login_page_blocks.login_with_wrong_email()
        login_page.error_auth_message.should_be_visible()
        login_page.error_auth_message_text.should_have_text('Invalid email or password. Please try again.')

    @pytest.mark.regression
    def test_login_with_invalid_email_format(self, login_page, login_page_blocks) -> None:
        login_page.open_login_page()
        login_page_blocks.login_with_invalid_email()
        validation_message = login_page.email_input.get_html5_validation_message()
        assert '@' in validation_message, f"Expected validation message containing '@', got: '{validation_message}'"



