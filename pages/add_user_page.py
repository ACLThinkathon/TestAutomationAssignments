from pages.base_page import BasePage
from config.config import Config


class AddUserPage(BasePage):
    """Represents Admin > User Management > Users > Add (the "Add User" form)."""

    EMPLOYEE_NAME_INPUT = "input[placeholder='Type for hints...']"
    USERNAME_INPUT = "//label[normalize-space(text())='Username']/ancestor::div[contains(@class,'oxd-input-group')]//input"
    PASSWORD_INPUT = "//label[normalize-space(text())='Password']/ancestor::div[contains(@class,'oxd-input-group')]//input"
    CONFIRM_PASSWORD_INPUT = "//label[normalize-space(text())='Confirm Password']/ancestor::div[contains(@class,'oxd-input-group')]//input"
    SAVE_BUTTON = "button[type='submit']"
    CANCEL_BUTTON = "button[type='button']:has-text('Cancel')"
    FIELD_ERROR = ".oxd-input-group__message"

    @staticmethod
    def _select_by_label(label_text: str) -> str:
        return (
            f"//label[normalize-space(text())='{label_text}']"
            "/ancestor::div[contains(@class,'oxd-input-group')]"
            "//div[contains(@class,'oxd-select-text')]"
        )

    def navigate(self) -> "AddUserPage":
        self.goto(Config.ADD_USER_URL)
        return self

    def select_user_role(self, role: str) -> None:
        self.select_oxd_dropdown_option(self._select_by_label("User Role"), role)

    def select_employee(self, search_term: str) -> str:
        return self.select_autocomplete_option(self.EMPLOYEE_NAME_INPUT, search_term)

    def select_status(self, status: str) -> None:
        self.select_oxd_dropdown_option(self._select_by_label("Status"), status)

    def enter_username(self, username: str) -> None:
        self.fill(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        self.fill(self.PASSWORD_INPUT, password)

    def enter_confirm_password(self, password: str) -> None:
        self.fill(self.CONFIRM_PASSWORD_INPUT, password)

    def click_save(self) -> None:
        self.click(self.SAVE_BUTTON)

    def click_cancel(self) -> None:
        self.click(self.CANCEL_BUTTON)

    def add_user(
        self,
        user_role: str,
        employee_search_term: str,
        status: str,
        username: str,
        password: str,
    ) -> None:
        """High-level workflow method composing the smaller actions above.

        Keeping this here (rather than only in the test) lets any future
        test reuse the exact same, already-validated flow for creating a
        user in a single call.
        """
        self.select_user_role(user_role)
        self.select_employee(employee_search_term)
        self.select_status(status)
        self.enter_username(username)
        self.enter_password(password)
        self.enter_confirm_password(password)
        self.click_save()

    def is_success_toast_visible(self) -> bool:
        try:
            message = self.wait_for_toast()
            return "success" in message.lower()
        except Exception:
            return False

    def has_field_error(self) -> bool:
        return self.is_visible(self.FIELD_ERROR, timeout=5000)
