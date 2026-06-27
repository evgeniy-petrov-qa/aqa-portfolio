from playwright.sync_api import Page

from automatedtests.pages.pages.nomads_main_page import NomadsMainPage


class NomadsMainPageBlocks(NomadsMainPage):

    def click_get_insured_in_new_tab(self) -> Page:
        """
        Click «Get insured» and return the newly opened Page.

        :return: New Page with SafetyWing insurance site.
        """
        with self.wait_for_new_tab() as tab_info:
            self.click_get_insured()
        return tab_info.value
