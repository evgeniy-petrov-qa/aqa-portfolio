"""Page Object for nomads.com."""
from automatedtests.pages.element import Element
from automatedtests.pages.pages.common_page import CommonPage


class NomadsMainPage(CommonPage):
    """nomads.com main page."""

    # ------------------------------------------------------------------
    # Hero section
    # ------------------------------------------------------------------

    @property
    def get_insured_btn(self) -> Element:
        """«Get insured» CTA button in the hero section."""
        return Element(self.page.get_by_alt_text("Get insured"))

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open_nomads(self) -> None:
        """Navigate to nomads.com."""
        self.open_url(self.urls.nomads)

    def click_get_insured(self) -> None:
        """Click «Get insured» button."""
        self.get_insured_btn.click()