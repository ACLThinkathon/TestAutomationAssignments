import allure

from pages.base_page import BasePage
from config.config import Config


class EmployeeListPage(BasePage):
    """Represents PIM > Employee List (the employee search/results list)."""

    EMPLOYEE_NAME_INPUT = "input[placeholder='Type for hints...']"
    SEARCH_BUTTON = "button:has-text('Search')"
    RESET_BUTTON = "button:has-text('Reset')"
    TABLE_ROW = ".oxd-table-body .oxd-table-row"
    EDIT_BUTTON = "button:has(i.bi-pencil-fill)"

    def navigate(self) -> "EmployeeListPage":
        self.goto(Config.EMPLOYEE_LIST_URL)
        return self

    def search_by_employee_name(self, full_name: str) -> None:
        self.select_autocomplete_option(self.EMPLOYEE_NAME_INPUT, full_name)
        self.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def is_employee_listed(self, name: str) -> bool:
        row_selector = f"{self.TABLE_ROW}:has-text('{name}')"
        return self.is_visible(row_selector, timeout=self.timeout)

    def row_count(self) -> int:
        return self.count(self.TABLE_ROW)

    @allure.step("Open employee record: {name}")
    def open_employee(self, name: str) -> None:
        """Opens the matching row's Personal Details page (via its edit
        icon) -- the same page MyInfoPage represents when it's the
        logged-in user's own record, so MyInfoPage's field getters can be
        reused to inspect any employee this way.
        """
        row = self.page.locator(self.TABLE_ROW, has_text=name).first
        row.locator(self.EDIT_BUTTON).first.click(timeout=self.timeout)
        self.page.wait_for_load_state("networkidle")
