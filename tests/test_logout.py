import allure
import pytest

pytestmark = allure.feature("Logout")


@allure.story("Logout")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("User can log out from the profile picture menu after navigating to PIM")
@pytest.mark.smoke
def test_recorded_flow(login_page, dashboard_page):
    """Logout flow via Dashboard menu.

    This test reproduces the recorded navigation steps:
    login via the login page, open the PIM module, open the profile picture,
    and click the Logout menu item.
    """
    # Login
    login_page.navigate()
    login_page.login(username="Admin", password="admin123")

    # Navigate to PIM module
    dashboard_page.open_module("PIM")

    # Logout via user dropdown/profile picture menu
    dashboard_page.logout()
