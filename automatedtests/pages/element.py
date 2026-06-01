"""
Element class for interacting with a single DOM node.

Encapsulates all interactions with a specific page element:
clicks, text input, data retrieval, and state assertions.

Used in Page Objects as the return type of locators::

    @property
    def submit_button(self) -> Element:
        return Element(self.page.locator("#submit"))

    # in a test:
    login_page.submit_button.click()
"""

from typing import Optional
from playwright.sync_api import Locator, expect, TimeoutError as PlaywrightTimeoutError


class Element():
    """
    Wrapper around Playwright Locator.

    Represents a single DOM element and provides methods
    for interaction and state assertions.
    """

    DEFAULT_TIMEOUT: int = 20_000

    def     __init__(self, locator: Locator) -> None:
        """
        :param locator: Playwright Locator pointing to the specific element.
        """
        self.locator = locator

    # ------------------------------------------------------------------
    # Interactions
    # ------------------------------------------------------------------

    def click(self, timeout: Optional[int] = None) -> None:
        """
        Click the element.

        :param timeout: Timeout waiting for clickability in ms.
        """
        self.locator.click(timeout=timeout or self.DEFAULT_TIMEOUT)

    def fill(self, value: str, timeout: Optional[int] = None) -> None:
        """
        Clear the field and type text.

        :param value: Value to type.
        :param timeout: Timeout in ms.
        """
        self.locator.fill(value, timeout=timeout or self.DEFAULT_TIMEOUT)

    def select_option(self, value: str) -> None:
        """
        Select an option in a <select> by value.

        :param value: Option value to select.
        """
        self.locator.select_option(value)

    def check(self) -> None:
        """Check a checkbox or radio button."""
        self.locator.check()

    def uncheck(self) -> None:
        """Uncheck a checkbox."""
        self.locator.uncheck()

    def hover(self) -> None:
        """Hover the mouse over the element."""
        self.locator.hover()

    def press(self, key: str) -> None:
        """
        Press a key in the context of the element.

        :param key: Key name, e.g. 'Enter', 'Tab', 'Escape'.
        """
        self.locator.press(key)

    def scroll_into_view(self) -> None:
        """Scroll the page to bring the element into view."""
        self.locator.scroll_into_view_if_needed()

    # ------------------------------------------------------------------
    # Data retrieval
    # ------------------------------------------------------------------

    def get_text(self) -> str:
        """
        Get the visible text of the element.

        :return: Text content of the element.
        """
        return self.locator.inner_text()

    def get_attribute(self, attribute: str) -> Optional[str]:
        """
        Get the value of an HTML attribute.

        :param attribute: Attribute name, e.g. 'href', 'class', 'data-id'.
        :return: Attribute value or None.
        """
        return self.locator.get_attribute(attribute)

    def get_value(self) -> str:
        """
        Get the current value of an input field (<input>, <textarea>).

        :return: Current field value.
        """
        return self.locator.input_value()

    def get_html5_validation_message(self) -> str:
        """
        Get the native HTML5 validation message for the field.

        :return: Validation message text, or empty string if validation did not trigger.
        """
        return self.locator.evaluate("el => el.validationMessage")

    # ------------------------------------------------------------------
    # Waits
    # ------------------------------------------------------------------

    def wait_for_visible(self, timeout: Optional[int] = None) -> None:
        """
        Wait until the element becomes visible.

        :param timeout: Timeout in ms.
        """
        self.locator.wait_for(state="visible", timeout=timeout or self.DEFAULT_TIMEOUT)

    def wait_for_hidden(self, timeout: Optional[int] = None) -> None:
        """
        Wait until the element is hidden or removed from the DOM.

        :param timeout: Timeout in ms.
        """
        self.locator.wait_for(state="hidden", timeout=timeout or self.DEFAULT_TIMEOUT)

    # ------------------------------------------------------------------
    # State assertions
    # ------------------------------------------------------------------

    def should_be_visible(self, timeout: Optional[int] = None) -> None:
        """
        Assert that the element is visible on the page.

        :param timeout: Timeout in ms.
        """
        expect(self.locator).to_be_visible(timeout=timeout or self.DEFAULT_TIMEOUT)

    def should_not_be_visible(self, timeout: Optional[int] = None) -> None:
        """
        Assert that the element is NOT visible on the page.

        :param timeout: Timeout in ms.
        """
        expect(self.locator).not_to_be_visible(timeout=timeout or self.DEFAULT_TIMEOUT)

    def should_have_text(self, text: str, timeout: Optional[int] = None) -> None:
        """
        Assert that the element contains the expected text (substring match).

        :param text: Expected text.
        :param timeout: Timeout in ms.
        """
        expect(self.locator).to_contain_text(text, timeout=timeout or self.DEFAULT_TIMEOUT)

    def should_have_attribute(self, attribute: str, value: str, timeout: Optional[int] = None) -> None:
        """
        Assert that the element has an attribute with the expected value.

        :param attribute: Attribute name, e.g. 'href', 'class', 'data-id'.
        :param value: Expected attribute value.
        :param timeout: Timeout in ms.
        """
        expect(self.locator).to_have_attribute(attribute, value, timeout=timeout or self.DEFAULT_TIMEOUT)

    def should_be_enabled(self, timeout: Optional[int] = None) -> None:
        """
        Assert that the element is enabled (not disabled).

        :param timeout: Timeout in ms.
        """
        expect(self.locator).to_be_enabled(timeout=timeout or self.DEFAULT_TIMEOUT)

    def should_be_disabled(self, timeout: Optional[int] = None) -> None:
        """
        Assert that the element is disabled.

        :param timeout: Timeout in ms.
        """
        expect(self.locator).to_be_disabled(timeout=timeout or self.DEFAULT_TIMEOUT)

    def should_be_checked(self, timeout: Optional[int] = None) -> None:
        """
        Assert that the checkbox or radio button is checked.

        :param timeout: Timeout in ms.
        """
        expect(self.locator).to_be_checked(timeout=timeout or self.DEFAULT_TIMEOUT)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def is_visible(self) -> bool:
        """
        Check element visibility without raising an exception.

        Use for conditional logic inside page methods::

            if self.cookie_banner.is_visible():
                self.cookie_banner.click()

        :return: True if the element is visible, False otherwise.
        """
        try:
            return self.locator.is_visible()
        except PlaywrightTimeoutError:
            return False

    def find_child(self, selector: str) -> "Element":
        """
        Find a child element within the current element.

        :param selector: CSS or XPath selector of the child element.
        :return: New Element for the found child node.
        """
        return Element(self.locator.locator(selector))
