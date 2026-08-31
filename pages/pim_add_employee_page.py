from pages.base_page import BasePage
from config.config import Config


class PimAddEmployeePage(BasePage):
    """Represents PIM > Add Employee (the "Add Employee" form)."""

    FIRST_NAME_INPUT = "input[name='firstName']"
    LAST_NAME_INPUT = "input[name='lastName']"
    SAVE_BUTTON = "button[type='submit']"

    def navigate(self) -> "PimAddEmployeePage":
        self.goto(Config.ADD_EMPLOYEE_URL)
        return self

    def add_employee(self, first_name: str, last_name: str) -> None:
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.click(self.SAVE_BUTTON)

    def is_saved(self, timeout: int | None = None) -> bool:
        """Saving redirects (asynchronously) to the new employee's Personal
        Details page, so waiting for that URL is the reliable success signal
        rather than the success toast, which can disappear before assertion.
        """
        try:
            self.page.wait_for_url("**/viewPersonalDetails/**", timeout=timeout or self.timeout)
            return True
        except Exception:
            return False
