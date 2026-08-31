from pages.base_page import BasePage


class MyInfoPage(BasePage):
    """Represents My Info > Personal Details (the logged-in user's own profile)."""

    TOP_MENU_MY_INFO = "a.oxd-main-menu-item:has-text('My Info')"
    MIDDLE_NAME_INPUT = "input[name='middleName']"
    SAVE_BUTTON = "button:has-text('Save')"

    def navigate(self) -> "MyInfoPage":
        self.click(self.TOP_MENU_MY_INFO)
        self.page.wait_for_load_state("networkidle")
        return self

    def get_middle_name(self) -> str:
        return self.get_value(self.MIDDLE_NAME_INPUT)

    def update_middle_name(self, middle_name: str) -> None:
        self.fill(self.MIDDLE_NAME_INPUT, middle_name)
        self.click(self.SAVE_BUTTON)

    def is_success_toast_visible(self) -> bool:
        try:
            message = self.wait_for_toast()
            return "success" in message.lower()
        except Exception:
            return False
