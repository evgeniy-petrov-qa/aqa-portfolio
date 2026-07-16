from automatedtests.pages.blocks.common_page_block import CommonPageBlocks
from automatedtests.pages.element import Element


class AfAppsPage(CommonPageBlocks):

    # ------------------------------------------------------------------
    # Workspaces form
    # ------------------------------------------------------------------

    @property
    def add_workspace_form(self) -> Element:
        """Add workspace form."""
        return Element(self.page.get_by_text("Add workspace"))

    @property
    def enter_workspace_name_field(self) -> Element:
        """Workspace name input field."""
        modal = self.page.get_by_test_id("modal_content")
        return Element(modal.get_by_placeholder("Enter name"))

    @property
    def add_workspace_button(self) -> Element:
        """Add workspace button."""
        return Element(self.page.get_by_role("button", name="Add workspace"))

    @property
    def search_app_field(self) -> Element:
        """App search input field."""
        return Element(self.page.get_by_placeholder("Enter app name, developer, or direct store link"))

    @property
    def search_button(self) -> Element:
        """Search button."""
        return Element(self.page.get_by_role("button", name="Search"))

    @property
    def my_apps_menu(self) -> Element:
        """Apps sidebar menu item."""
        return Element(self.page.locator('[data-selenide-sidebar-page="apps"]'))

    @property
    def delete_workspace_button(self) -> Element:
        """Delete workspace confirmation button."""
        return Element(self.page.get_by_role("button", name="Delete workspace"))

    @property
    def delete_workspace_field(self) -> Element:
        """Workspace name confirmation input in the delete modal."""
        return Element(self.page.get_by_placeholder("Enter workspace name"))

    def add_app_button_by_app_id(self, app_id: str) -> Element:
        """'Add app' button inside the search result card matched by app_id.

        app_id is the most reliable anchor — visible on the page and unique across results.
        """
        app_id_element = self.page.get_by_text(app_id, exact=True)

        result_card = app_id_element.locator(
            "xpath=ancestor::div[.//button[normalize-space()='Add app']][1]"
        )

        return Element(result_card.get_by_role("button", name="Add app", exact=True))

    def app_title(self, app_title: str) -> Element:
        """App title element matched by exact text."""
        return Element(self.page.get_by_text(app_title, exact=True))

    def delete_button_for_workspace(self, workspace_name: str) -> Element:
        """Delete button inside the workspace card matched by workspace_name.

        The button has no aria-label or test-id, so we walk up the DOM via xpath ancestor
        to the nearest div with exactly 2 buttons (settings + delete). Last button = delete.
        """
        workspace_name_element = self.page.get_by_text(workspace_name, exact=True)

        workspace_card = workspace_name_element.locator(
            "xpath=ancestor::div[count(.//button)=2][1]"
        )

        return Element(workspace_card.get_by_role("button").last)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open_apps_page(self) -> None:
        """Open Appfollow apps page."""
        self.open_url(f"{self.urls.appfollow_apps}")