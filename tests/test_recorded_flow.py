import allure
import pytest

from config.config import BASE_URL
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.employee_list_page import EmployeeListPage
from test_script_helpers import _run_genai_validation


pytestmark = allure.feature("Recorded Flow")


@allure.story("Recorded Flow")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Recorded OrangeHRM flow with search and logout")
@pytest.mark.smoke
def test_recorded_flow(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    employee_list_page = EmployeeListPage(page)

    # Navigate to login and sign in as Admin
    login_page.navigate()
    login_page.login("Admin", "admin123")

    # Open PIM module from the dashboard
    dashboard_page.open_module("PIM")

    # Search employees by name and validate results
    employee_list_page.search_by_employee_name("test")
    _run_genai_validation(page, 'Verify search results show "test" text')

    # Logout from the application
    dashboard_page.logout()
