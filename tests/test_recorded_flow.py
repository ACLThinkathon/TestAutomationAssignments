import pytest

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_users_page import AdminUsersPage
from test_script_helpers import _run_genai_validation


@pytest.mark.regression
def test_recorded_flow(logged_in_page):
    page = logged_in_page

    # Use page objects instead of raw Playwright calls
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    admin_users_page = AdminUsersPage(page)

    # Navigate to login and authenticate (mirrors script's manual login)
    login_page.navigate()
    login_page.login("Admin", "admin123")

    # Navigate to Admin module via dashboard top menu
    assert dashboard_page.is_loaded()
    dashboard_page.open_module("Admin")

    # Search for the "Admin" user in the System Users list
    admin_users_page.search_by_username("Admin")

    # GenAI validation on the fact that at least one result row is visible
    assert admin_users_page.is_any_result_visible()
    _run_genai_validation(page, "Validate searched User is displayed")
