from playwright.sync_api import ConsoleMessage, Page

from automatedtests.pages.pages.common_page import CommonPage
from automatedtests.pages.settings import URLs


class CommonPageBlocks(CommonPage):
    """Universal base class for all page objects."""

    def __init__(self, page: Page, urls: URLs) -> None:
        super().__init__(page, urls)
        self._console_errors: list[str] = []
        self.page.on("console", self._capture_error)
        self.page.on("framenavigated", self._on_navigation)

    def _capture_error(self, msg: ConsoleMessage) -> None:
        if msg.type == "error":
            self._console_errors.append(msg.text)

    def _on_navigation(self, _) -> None:
        self._console_errors.clear()

    @property
    def console_errors(self) -> list[str]:
        return list(self._console_errors)

    def has_console_errors(self) -> bool:
        return bool(self._console_errors)
