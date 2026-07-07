from pages.base_page import BasePage
from config.config import Config


class LoginPage(BasePage):
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_ALERT = ".oxd-alert-content-text"

    def navigate(self) -> "LoginPage":
        self.goto(Config.LOGIN_URL)
        return self

    def login(self, username: str, password: str) -> None:
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_ALERT)

    def has_error_message(self) -> bool:
        return self.is_visible(self.ERROR_ALERT, timeout=5000)
