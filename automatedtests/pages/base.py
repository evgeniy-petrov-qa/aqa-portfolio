
from typing import Optional
from playwright.sync_api import Page, expect, FrameLocator, BrowserContext


class BasePage:
    """
    Base class for all Page Objects.

    Encapsulates browser tab interactions:
    navigation, page properties, tab and iframe switching.

    Element interactions (click, fill, assertions) are delegated to Element.
    """

    DEFAULT_TIMEOUT: int = 20_000
 
    def __init__(self, page: Page) -> None:
        """
        :param page: Playwright Page instance, injected via fixture.
        """
        self.page = page
 
    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def open_url(self, url: str) -> None:
        """
        Navigate to URL and wait for DOM to load.

        :param url: Absolute or relative URL.
        """
        self.page.goto(url, wait_until="domcontentloaded", timeout=self.DEFAULT_TIMEOUT)
 
    def reload(self) -> None:
        """Reload the current page."""
        self.page.reload(wait_until="domcontentloaded", timeout=self.DEFAULT_TIMEOUT)
 
    def go_back(self) -> None:
        """Navigate to the previous page in browser history."""
        self.page.go_back(wait_until="domcontentloaded", timeout=self.DEFAULT_TIMEOUT)
 
    # ------------------------------------------------------------------
    # Page properties
    # ------------------------------------------------------------------

    @property
    def current_url(self) -> str:
        """Current page URL."""
        return self.page.url

    @property
    def title(self) -> str:
        """Current page title."""
        return self.page.title()

    # ------------------------------------------------------------------
    # Context switching
    # ------------------------------------------------------------------
 
    def switch_to_tab(self, index: int) -> None:
        """
        Switch to a browser tab by index (0-based).

        :param index: Tab index.
        :raises IndexError: If no tab with the given index exists.
        """
        self.page = self.page.context.pages[index]

    def wait_for_new_tab(self) -> BrowserContext:
        """
        Return a context manager that resolves to a newly opened Page.

        Usage::

            with self.wait_for_new_tab() as tab_info:
                self.some_link.click()
            new_page = tab_info.value

        :return: EventContextManager yielding the new Page.
        """
        return self.page.context.expect_page()
 
    def get_iframe(self, selector: str) -> FrameLocator:
        """
        Get a FrameLocator for working with elements inside an iframe.

        :param selector: CSS selector of the iframe, e.g. 'iframe#payment'.
        :return: FrameLocator — use like a page to locate elements inside the frame.

        Example::

            frame = self.get_iframe('iframe#captcha')
            frame.locator('#checkbox').click()
        """
        return self.page.frame_locator(selector)
 
    # ------------------------------------------------------------------
    # Page-level waits
    # ------------------------------------------------------------------

    def wait_for_url(self, url_pattern: str, timeout: Optional[int] = None) -> None:
        """
        Wait until the URL matches the given pattern (string or regex).

        :param url_pattern: Expected URL or regex pattern.
        :param timeout: Timeout in ms.
        """
        self.page.wait_for_url(url_pattern, timeout=timeout or self.DEFAULT_TIMEOUT)
 
    def wait_for_network_idle(self, timeout: Optional[int] = None) -> None:
        """
        Wait for all network requests to complete.

        :param timeout: Timeout in ms.
        """
        self.page.wait_for_load_state("networkidle", timeout=timeout or self.DEFAULT_TIMEOUT)
 
    # ------------------------------------------------------------------
    # Page assertions
    # ------------------------------------------------------------------

    def should_have_url(self, url_pattern: str, timeout: Optional[int] = None) -> None:
        """
        Assert that the current URL matches the given pattern.

        :param url_pattern: Expected URL or regex pattern.
        :param timeout: Timeout in ms.
        """
        expect(self.page).to_have_url(url_pattern, timeout=timeout or self.DEFAULT_TIMEOUT)
 
    def should_have_title(self, title_pattern: str, timeout: Optional[int] = None) -> None:
        """
        Assert that the page title matches the given pattern.

        :param title_pattern: Expected title or regex pattern.
        :param timeout: Timeout in ms.
        """
        expect(self.page).to_have_title(title_pattern, timeout=timeout or self.DEFAULT_TIMEOUT)
 
    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def take_screenshot(self) -> bytes:
        """
        Take a screenshot of the current page.

        :return: Screenshot as bytes (PNG).
        """
        return self.page.screenshot(full_page=True)