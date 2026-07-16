import random

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

    @staticmethod
    def generate_workflow_name() -> str:
        """Generates a random workflow name in the format 'test_{12345}'."""
        return f"test_{random.randint(10000, 99999)}"


    @staticmethod
    def application_name() -> str:
        return "chess.com"

    @staticmethod
    def application_id() -> str:
        return "com.chess"

    @staticmethod
    def application_title() -> str:
        return "Chess - Play and Learn Online"

