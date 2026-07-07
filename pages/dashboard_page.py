from pages.base_page import BasePage


class DashboardPage(BasePage):
    PAGE_HEADER = ".oxd-topbar-header-breadcrumb h6"
    USER_DROPDOWN = ".oxd-userdropdown-tab"
    LOGOUT_LINK = "a:has-text('Logout')"
    TOP_MENU_ITEM = "a.oxd-topbar-body-nav-tab-item:has-text('{name}')"

    def is_loaded(self) -> bool:
        return self.is_visible(self.PAGE_HEADER) and "dashboard" in self.current_url()

    def get_header_text(self) -> str:
        return self.get_text(self.PAGE_HEADER)

    def open_module(self, module_name: str) -> None:
        self.click(self.TOP_MENU_ITEM.format(name=module_name))

    def logout(self) -> None:
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_LINK)
