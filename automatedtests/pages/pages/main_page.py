"""
Page Object for the QA Playground main page.

URL: https://qaplayground.com/
"""
from automatedtests.pages.blocks.common_page_block import CommonPageBlocks
from automatedtests.pages.element import Element


class MainPage(CommonPageBlocks):
    """
    QA Playground main page.

    Contains the Hero section, section cards (Practice, Bank Demo,
    Study Tracker), and a statistics block.
    """

    # ------------------------------------------------------------------
    # Header / Navbar
    # ------------------------------------------------------------------

    @property
    def nav_logo(self) -> Element:
        """QA PlayGround logo in the header."""
        return Element(self.page.locator("header a[href='/']").first)

    # ------------------------------------------------------------------
    # Footer
    # ------------------------------------------------------------------

    @property
    def footer_login_link(self) -> Element:
        """«Login» link in the footer."""
        return Element(self.page.locator("footer a[href='/login']"))

    @property
    def footer_privacy_link(self) -> Element:
        """«Privacy Policy» link in the footer."""
        return Element(self.page.locator("footer a[href='/privacy-policy']"))

    @property
    def footer_copyright(self) -> Element:
        """Copyright text block in the footer."""
        return Element(self.page.locator("footer").get_by_text("QA Playground. All rights reserved"))

    # ------------------------------------------------------------------
    # Hero section
    # ------------------------------------------------------------------

    @property
    def hero_heading(self) -> Element:
        """Main heading «Master Automation Testing With QA PlayGround»."""
        return Element(self.page.get_by_role("heading", name="Master Automation Testing With QA PlayGround"))

    @property
    def hero_get_started_btn(self) -> Element:
        """«Get Started» button in the hero section."""
        return Element(self.page.get_by_role("link", name="Get Started"))

    @property
    def hero_watch_demo_btn(self) -> Element:
        """«Watch Demo» button in the hero section."""
        return Element(self.page.get_by_role("link", name="Watch Demo"))

    # ------------------------------------------------------------------
    # Section cards
    # ------------------------------------------------------------------

    @property
    def card_practice_link(self) -> Element:
        """«Start Practicing» link in the Practice Elements card."""
        return Element(self.page.get_by_role("link", name="Start Practicing"))

    @property
    def card_bank_demo_link(self) -> Element:
        """«Open Bank App» link in the Bank Demo card."""
        return Element(self.page.get_by_role("link", name="Open Bank App"))

    @property
    def card_study_tracker_link(self) -> Element:
        """«Track Your Progress» link in the Study Tracker card."""
        return Element(self.page.get_by_role("link", name="Track Your Progress"))

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def stat_active_users(self) -> Element:
        """«Active Users» statistics block."""
        return Element(self.page.get_by_text("Active Users"))

    @property
    def stat_practice_elements(self) -> Element:
        """«Practice Elements» statistics block."""
        return Element(self.page.get_by_text("Practice Elements"))

    @property
    def theme_toggle_btn(self) -> Element:
        """Light/dark theme toggle button in the navbar."""
        return Element(self.page.get_by_role("button", name="Toggle theme"))

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open_main_page(self) -> None:
        """
        Open the main page.

        :param url: Ignored — URL is fixed via urls.qa_playground.
        """
        super().open_url(self.urls.qa_playground)


    def click_toggle_theme(self) -> None:
        """Toggle the page theme (light ↔ dark)."""
        self.theme_toggle_btn.click()

    def get_theme(self) -> str:
        """
        Return the current page theme.

        :return: 'dark' or 'light'.
        """
        classes = self.page.locator("html").get_attribute("class") or ""
        return "dark" if "dark" in classes else "light"

    def set_theme(self, theme: str) -> None:
        """
        Set the desired theme if it is not already active.

        Used as a precondition — clicks the button only if the current theme differs.

        :param theme: Target theme — 'light' or 'dark'.
        """
        if self.get_theme() != theme:
            self.click_toggle_theme()
