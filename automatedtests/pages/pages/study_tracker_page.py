"""
Page Object for the QA Study Tracker Dashboard page.

URL: https://qaplayground.com/study-tracker/dashboard
"""
from automatedtests.pages.blocks.common_page_block import CommonPageBlocks
from automatedtests.pages.element import Element


class StudyTrackerPage(CommonPageBlocks):
    """QA Study Tracker dashboard page."""

    # ------------------------------------------------------------------
    # Heading
    # ------------------------------------------------------------------

    @property
    def heading(self) -> Element:
        """Main heading «QA Study Tracker»."""
        return Element(self.page.get_by_role("heading", name="QA Study Tracker"))

    # ------------------------------------------------------------------
    # Sidebar navigation
    # ------------------------------------------------------------------

    @property
    def sidebar_dashboard_link(self) -> Element:
        """«Dashboard» link in the sidebar (active page)."""
        return Element(self.page.get_by_role("link", name="Dashboard"))

    @property
    def sidebar_daily_tracker_link(self) -> Element:
        """«Daily Tracker» link in the sidebar."""
        return Element(self.page.get_by_role("link", name="Daily Tracker"))

    @property
    def sidebar_syllabus_link(self) -> Element:
        """«Syllabus Manager» link in the sidebar."""
        return Element(self.page.get_by_role("link", name="Syllabus Manager"))

    @property
    def sidebar_resources_link(self) -> Element:
        """«Resources» link in the sidebar."""
        return Element(self.page.get_by_role("link", name="Resources"))

    @property
    def sidebar_interview_practice_link(self) -> Element:
        """«Interview Practice» link in the sidebar."""
        return Element(self.page.get_by_role("link", name="Interview Practice"))

    @property
    def sidebar_collapse_btn(self) -> Element:
        """Collapse sidebar button."""
        return Element(self.page.get_by_role("button", name="Collapse sidebar"))

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self) -> None:
        """Open the Study Tracker dashboard."""
        super().open_url(f"{self.urls.qa_playground}/study-tracker/dashboard")