import pytest

@pytest.mark.ui
class TestMainPage:

    @pytest.mark.regression
    @pytest.mark.parametrize("expected_theme", ["dark", "light"])
    def test_toggle_changes_theme_to_opposite(self, main_page, expected_theme) -> None:
        main_page.open_main_page()
        main_page.set_theme(expected_theme)
        main_page.click_toggle_theme()
        assert main_page.get_theme() != expected_theme, f"Theme did not change after click"

    @pytest.mark.smoke
    def test_click_login_link_navigates_to_login_page(self, main_page, login_page) -> None:
        main_page.open_main_page()
        main_page.footer_login_link.click()
        main_page.should_have_url(f"{main_page.urls.qa_playground}/login")
        login_page.sign_in_button.should_be_visible()

    @pytest.mark.regression
    def test_logo_click_navigates_to_home(self, main_page) -> None:
        main_page.open_main_page()
        main_page.footer_login_link.click()
        main_page.nav_logo.click()
        main_page.should_have_url(f"{main_page.urls.qa_playground}/")
        main_page.hero_heading.should_be_visible()

    @pytest.mark.regression
    def test_footer_copyright_is_visible(self, main_page) -> None:
        main_page.open_main_page()
        main_page.footer_copyright.should_be_visible()

    @pytest.mark.regression
    def test_footer_privacy_link_navigates_to_privacy_policy(self, main_page) -> None:
        main_page.open_main_page()
        main_page.footer_privacy_link.click()
        main_page.should_have_url(f"{main_page.urls.qa_playground}/privacy-policy")
