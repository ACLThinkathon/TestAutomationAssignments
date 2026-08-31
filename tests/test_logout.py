"""Logout scenario: ending an authenticated session from the Dashboard."""
import allure
import pytest

from pages.login_page import LoginPage

pytestmark = allure.feature("Authentication")


@allure.story("Logout")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Logout returns to the login page")
@pytest.mark.smoke
def test_logout_returns_to_login_page(logged_in_page, dashboard_page):
    assert dashboard_page.is_loaded()

    dashboard_page.logout()

    login_page = LoginPage(logged_in_page)
    assert "auth/login" in login_page.current_url(), "Expected to be redirected to the login page after logout"
    assert login_page.is_visible(LoginPage.LOGIN_BUTTON), "Expected the login form to be visible after logout"
