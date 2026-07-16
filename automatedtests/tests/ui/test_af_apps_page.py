import pytest

from automatedtests.data.test_data import TestData


@pytest.mark.appfollow
class TestAfAppsPage:

    def test_add_app_to_new_workspace(self, af_login_page_blocks, af_apps_page_blocks):
        workspace_name = TestData.generate_workflow_name()
        try:
            af_login_page_blocks.appfollow_log_in()
            af_apps_page_blocks.open_apps_page()
            af_apps_page_blocks.add_new_workspace(workspace_name=workspace_name)
            af_apps_page_blocks.add_new_app(app_name=TestData.application_name(), app_id=TestData.application_id())
            af_apps_page_blocks.app_title(app_title=TestData.application_title()).should_be_visible()
        finally:
            af_apps_page_blocks.clear_workspace(workspace_name=workspace_name)
