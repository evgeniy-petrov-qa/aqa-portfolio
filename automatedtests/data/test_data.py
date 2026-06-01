class TestData:

    @staticmethod
    def wrong_password() -> str:
        return "WrongPass123!"

    @staticmethod
    def wrong_email() -> str:
        return "notexist11111@example.com"

    @staticmethod
    def invalid_email() -> str:
        return "not-an-email"