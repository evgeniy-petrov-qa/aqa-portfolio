from automatedtests.pages.pages.af_apps_page import AfAppsPage


class AfAppsPageBlocks(AfAppsPage):

    def add_new_workspace(self, workspace_name: str) -> None:
        self.add_workspace_form.click()
        self.enter_workspace_name_field.fill(workspace_name)
        self.add_workspace_button.click()


    def add_new_app(self, app_name: str, app_id: str) -> None:
        self.search_app_field.fill(app_name)
        self.search_button.click()
        self.add_app_button_by_app_id(app_id).click()
        self.my_apps_menu.click()

    def clear_workspace(self, workspace_name: str) -> None:
        self.open_apps_page()
        delete_btn = self.delete_button_for_workspace(workspace_name)
        try:
            delete_btn.wait_for_visible()
        except Exception:
            return
        delete_btn.click()
        self.delete_workspace_field.fill(workspace_name)
        self.delete_workspace_button.click()