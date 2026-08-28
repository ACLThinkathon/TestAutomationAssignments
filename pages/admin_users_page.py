from pages.base_page import BasePage
from config.config import Config


class AdminUsersPage(BasePage):
    """Represents Admin > User Management > Users (the System Users list)."""

    ADD_BUTTON = "button:has-text('Add')"
    USERNAME_FILTER = "//label[normalize-space(text())='Username']/ancestor::div[contains(@class,'oxd-input-group')]//input"
    SEARCH_BUTTON = "button:has-text('Search')"
    RESET_BUTTON = "button:has-text('Reset')"
    RESULTS_COUNT_TEXT = ".oxd-table-header span"
    TABLE_ROW = ".oxd-table-body .oxd-table-row"
    NO_RECORDS_FOUND = ".oxd-table-body span:has-text('No Records Found')"

    def navigate(self) -> "AdminUsersPage":
        self.goto(Config.SYSTEM_USERS_URL)
        return self

    def click_add(self) -> None:
        self.click(self.ADD_BUTTON)

    def search_by_username(self, username: str) -> None:
        self.fill(self.USERNAME_FILTER, username)
        self.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def click_reset(self) -> None:
        self.click(self.RESET_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def get_username_filter_value(self) -> str:
        return self.get_value(self.USERNAME_FILTER)

    def is_user_listed(self, username: str) -> bool:
        row_selector = f"{self.TABLE_ROW}:has-text('{username}')"
        return self.is_visible(row_selector, timeout=self.timeout)

    def row_count(self) -> int:
        return self.count(self.TABLE_ROW)

    def is_any_result_visible(self) -> bool:
        """Return True if at least one user row is visible after a search.

        Waits for the row to render rather than checking the count
        instantly, since the table briefly re-mounts (and can report zero
        rows) while OrangeHRM re-fetches the unfiltered list.
        """
        return self.is_visible(self.TABLE_ROW, timeout=self.timeout)

    def has_no_results(self) -> bool:
        """Return True once the results table has settled on zero rows."""
        return self.wait_for_count(self.TABLE_ROW, 0)
