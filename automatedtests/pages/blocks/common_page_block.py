"""
Reusable UI blocks present on all QA Playground pages.

Contains locators and methods for the header (navbar) and footer.
"""
from automatedtests.pages.element import Element
from automatedtests.pages.pages.common_page import CommonPage


class CommonPageBlocks(CommonPage):
    """
    Extends CommonPage with shared site-wide UI blocks.

    All concrete pages inherit this class and get access to the header and footer.
    """

    # ------------------------------------------------------------------
    # Header / Navbar
    # ------------------------------------------------------------------

    @property
    def nav_logo(self) -> Element:
        """QA PlayGround logo in the header."""
        return Element(self.page.locator("header a[href='/']").first)

    @property
    def nav_home(self) -> Element:
        """«Home» link in the navbar."""
        return Element(self.page.get_by_role("link", name="Home"))

    @property
    def nav_study_tracker(self) -> Element:
        """«Study Tracker» link in the navbar."""
        return Element(self.page.get_by_role("link", name="Study Tracker"))

    @property
    def nav_bank_demo(self) -> Element:
        """«Bank Demo» link in the navbar."""
        return Element(self.page.get_by_role("link", name="Bank Demo"))

    @property
    def nav_practice(self) -> Element:
        """«Practice» link in the navbar."""
        return Element(self.page.get_by_role("link", name="Practice"))

    @property
    def nav_qa_tools(self) -> Element:
        """«QA Tools» link in the navbar."""
        return Element(self.page.get_by_role("link", name="QA Tools"))

    @property
    def nav_blog(self) -> Element:
        """«Blog» link in the navbar."""
        return Element(self.page.get_by_role("link", name="Blog"))

    # ------------------------------------------------------------------
    # Footer
    # ------------------------------------------------------------------

    @property
    def footer_logo(self) -> Element:
        """QA PlayGround logo in the footer."""
        return Element(self.page.locator("footer a[href='/']"))

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