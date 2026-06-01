import os

from automatedtests.data.test_data import TestData
from automatedtests.pages.pages.login_page import LoginPage


class LoginPageBlocks(LoginPage):


    def login_success(self, remember: bool = False) -> None:
        self.email_input.fill(os.environ["LOGIN"])
        self.password_input.fill(os.environ["PASSWORD"])
        if remember:
            self.remember_me_checkbox.check()
        self.sign_in_button.click()

    def login_with_wrong_email(self) -> None:
        self.email_input.fill(TestData.wrong_email())
        self.password_input.fill(os.environ["PASSWORD"])
        self.sign_in_button.click()

    def login_with_invalid_email(self) -> None:
        self.email_input.fill(TestData.invalid_email())
        self.sign_in_button.click()