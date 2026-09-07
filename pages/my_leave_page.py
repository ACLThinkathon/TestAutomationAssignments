from pages.base_page import BasePage
from config.config import Config


class MyLeavePage(BasePage):
    """Represents Leave > My Leave (the logged-in employee's own leave requests)."""

    TABLE_ROW = ".oxd-table-body .oxd-table-row"

    def navigate(self) -> "MyLeavePage":
        self.goto(Config.MY_LEAVE_URL)
        return self

    def _row_for_date(self, date_value: str):
        """`date_value` must match the table's own "yyyy-dd-mm" date format."""
        return self.page.locator(self.TABLE_ROW, has_text=date_value)

    def has_pending_approval_request(self, date_value: str) -> bool:
        row = self._row_for_date(date_value).first
        try:
            row.wait_for(state="visible", timeout=self.timeout)
        except Exception:
            return False
        return "pending approval" in row.inner_text().lower()
