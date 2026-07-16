"""
Intermediate class between BasePage and concrete page classes.

Connects BasePage to the urls fixture, giving concrete pages
ready-made methods for opening environments without knowing the config.
"""

from playwright.sync_api import Page

from automatedtests.pages.base import BasePage
from automatedtests.pages.settings import URLs


class CommonPage(BasePage):
    """
    Base class for all concrete page objects in the project.

    Receives validated URLs from the urls fixture (URLs model)
    and provides methods for opening specific environments.

    Example usage in a concrete page::

        class LoginPage(CommonPage):
            def open_login(self) -> None:
                self.open_crm()
    """

    def __init__(self, page: Page, urls: URLs) -> None:
        """
        :param page: Playwright Page instance, injected via fixture.
        :param urls: Validated environment URLs, injected via the urls fixture.
        """
        super().__init__(page)
        self.urls = urls
