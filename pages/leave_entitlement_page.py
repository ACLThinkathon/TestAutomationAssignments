from pages.base_page import BasePage
from config.config import Config


class LeaveEntitlementPage(BasePage):
    """Represents Leave > Entitlements > Add Leave Entitlement.

    Used purely as test setup: OrangeHRM's Apply Leave form only lists leave
    types that already have an entitlement balance for the employee ("No
    Leave Types with Leave Balance" otherwise), so a balance has to be
    granted here first before Apply Leave can be exercised.
    """

    EMPLOYEE_NAME_INPUT = "input[placeholder='Type for hints...']"
    LEAVE_TYPE_DROPDOWN = "//label[text()='Leave Type']/ancestor::div[contains(@class,'oxd-input-group')]//div[contains(@class,'oxd-select-text')]"
    LEAVE_PERIOD_DROPDOWN = "//label[text()='Leave Period']/ancestor::div[contains(@class,'oxd-input-group')]//div[contains(@class,'oxd-select-text')]"
    ENTITLEMENT_INPUT = "//label[text()='Entitlement']/ancestor::div[contains(@class,'oxd-input-group')]//input"
    SAVE_BUTTON = "button[type='submit']"
    CONFIRM_BUTTON = "button:has-text('Confirm')"

    def navigate(self) -> "LeaveEntitlementPage":
        self.goto(Config.ADD_LEAVE_ENTITLEMENT_URL)
        return self

    def add_entitlement(self, employee_name: str, leave_type: str, leave_period: str, days: str) -> None:
        self.select_autocomplete_option(self.EMPLOYEE_NAME_INPUT, employee_name)
        self.select_oxd_dropdown_option(self.LEAVE_TYPE_DROPDOWN, leave_type)
        self.select_oxd_dropdown_option(self.LEAVE_PERIOD_DROPDOWN, leave_period)
        self.fill(self.ENTITLEMENT_INPUT, days)
        self.click(self.SAVE_BUTTON)
        # Saving always asks for confirmation, even the first time a
        # balance is granted (current 0.00 -> new value).
        self.click(self.CONFIRM_BUTTON)
        self.page.wait_for_load_state("networkidle")
