import os

from automatedtests.pages.pages.af_login_page import AfLoginPage


class AfLoginPageBlock(AfLoginPage):

    def appfollow_log_in(self) -> None:
        self.open_login_page()
        self.log_in_button.click()
        self.email_input.fill(os.environ["AF_LOGIN"])
        self.password_input.fill(os.environ["AF_PASSWORD"])
        self.log_in_with_email_button.click()
        self.wait_for_url(url_pattern="**appfollow.io/apps/**")