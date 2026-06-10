from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from automatedtests.pages.blocks.common_page_block import CommonPageBlocks
from automatedtests.pages.element import Element


class LoginPage(CommonPageBlocks):
    """
    QA Playground login page.

    Contains the auth form: email and password fields,
    «Remember me» checkbox, sign-in button, and navigation links.
    """

    # ------------------------------------------------------------------
    # Auth form
    # ------------------------------------------------------------------

    @property
    def email_input(self) -> Element:
        """Email input field."""
        return Element(self.page.get_by_role("textbox", name="Email"))

    @property
    def password_input(self) -> Element:
        """Password input field."""
        return Element(self.page.get_by_role("textbox", name="Password"))

    @property
    def remember_me_checkbox(self) -> Element:
        """«Remember me for 30 days» checkbox."""
        return Element(self.page.get_by_role("checkbox", name="Remember me"))

    @property
    def sign_in_button(self) -> Element:
        """«Sign In» button."""
        return Element(self.page.get_by_role("button", name="Sign In"))

    @property
    def forgot_password_link(self) -> Element:
        """«Forgot password?» link."""
        return Element(self.page.get_by_role("link", name="Forgot password?"))

    @property
    def sign_up_link(self) -> Element:
        """«Sign up» link to the registration page."""
        return Element(self.page.get_by_role("link", name="Sign up"))

    @property
    def error_auth_message(self) -> Element:
        """Auth error message alert."""
        return Element(self.page.get_by_role("alert"))

    @property
    def error_auth_message_text(self) -> Element:
        """Auth error message text."""
        return Element(self.page.get_by_test_id("login-error"))

    @property
    def continue_with_email_button(self) -> Element:
        return Element(self.page.get_by_test_id("email-signin-button"))

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open_login_page(self, url: str = "") -> None:
        """
        Open the login page.

        :param url: Ignored — URL is fixed via urls.qa_playground.
        """
        super().open_url(f"{self.urls.qa_playground}/login")

    def click_continue_with_email_button(self) -> None:
        try:
            self.page.wait_for_load_state("networkidle", timeout=20_000)
        except PlaywrightTimeoutError:
            pass
        self.continue_with_email_button.click()



