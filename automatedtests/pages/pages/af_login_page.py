from automatedtests.pages.blocks.common_page_block import CommonPageBlocks
from automatedtests.pages.element import Element


class AfLoginPage(CommonPageBlocks):
    # ------------------------------------------------------------------
    # Auth form
    # ------------------------------------------------------------------

    @property
    def email_input(self) -> Element:
        """Email input field."""
        return Element(self.page.locator("#login-email"))

    @property
    def password_input(self) -> Element:
        """Password input field."""
        return Element(self.page.locator("#login-password"))

    @property
    def log_in_with_email_button(self) -> Element:
        """Log in with email button."""
        return Element(self.page.get_by_role("button", name="Log in with email"))

    @property
    def log_in_button(self) -> Element:
        """Log in with email button."""
        return Element(self.page.get_by_role("link", name="Log in"))

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open_login_page(self) -> None:
        """
        Open appfollow login page.
        """
        self.open_url(f"{self.urls.appfollow}")