from pages.base_page import BasePage
from config.config import Config


class ApplyLeavePage(BasePage):
    """Represents Leave > Apply (the "Apply Leave" form).

    Requires the employee to already have a leave balance for the chosen
    leave type -- see LeaveEntitlementPage for granting one.
    """

    LEAVE_TYPE_DROPDOWN = "//label[text()='Leave Type']/ancestor::div[contains(@class,'oxd-input-group')]//div[contains(@class,'oxd-select-text')]"
    FROM_DATE_INPUT = "//label[text()='From Date']/ancestor::div[contains(@class,'oxd-input-group')]//input"
    TO_DATE_INPUT = "//label[text()='To Date']/ancestor::div[contains(@class,'oxd-input-group')]//input"
    APPLY_BUTTON = "button[type='submit']:has-text('Apply')"
    FIELD_ERROR = ".oxd-input-group__message"

    def navigate(self) -> "ApplyLeavePage":
        self.goto(Config.APPLY_LEAVE_URL)
        return self

    def apply_leave(self, leave_type: str, from_date: str, to_date: str) -> None:
        """`from_date`/`to_date` must be in OrangeHRM's own "yyyy-dd-mm"
        format (matching the date field's placeholder), not ISO order.
        """
        self.select_oxd_dropdown_option(self.LEAVE_TYPE_DROPDOWN, leave_type)
        self.fill_oxd_date(self.FROM_DATE_INPUT, from_date)
        self.fill_oxd_date(self.TO_DATE_INPUT, to_date)
        self.click(self.APPLY_BUTTON)

    def is_success_toast_visible(self) -> bool:
        try:
            message = self.wait_for_toast()
            return "success" in message.lower()
        except Exception:
            return False

    def has_field_errors(self) -> bool:
        return self.is_visible(self.FIELD_ERROR, timeout=5000)
