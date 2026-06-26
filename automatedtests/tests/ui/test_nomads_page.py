import pytest


@pytest.mark.ui
class TestNomadsPage:

    @pytest.mark.regression
    def test_get_insured_opens_safetywing_in_new_tab(self, nomads_main_page, nomads_main_page_blocks) -> None:
        nomads_main_page.open_nomads()
        new_tab = nomads_main_page_blocks.click_get_insured_in_new_tab()
        assert "safetywing.com" in new_tab.url, f"Expected new tab to open safetywing.com, got: {new_tab.url}"