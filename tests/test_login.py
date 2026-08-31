"""Login scenarios for the Auth module."""
import allure
import pytest

from config.config import Config

pytestmark = allure.feature("Authentication")


@allure.story("Login")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Valid credentials navigate to the Dashboard")
@pytest.mark.smoke
def test_login_with_valid_credentials_navigates_to_dashboard(login_page, dashboard_page):
    login_page.navigate()
    login_page.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)

    assert dashboard_page.is_loaded(), "Expected the Dashboard to load after a valid login"
    assert dashboard_page.get_header_text() == "Dashboard"


@allure.story("Login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Invalid credentials show an error message")
@pytest.mark.regression
@pytest.mark.negative
def test_login_with_invalid_credentials_shows_error(login_page):
    login_page.navigate()
    login_page.login(Config.ADMIN_USERNAME, "wrong-password-123")

    assert login_page.has_error_message(), "Expected an error message for invalid credentials"
    assert "Invalid credentials" in login_page.get_error_message()


@allure.story("Login")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Empty credentials show required-field validation")
@pytest.mark.regression
@pytest.mark.negative
def test_login_with_empty_credentials_shows_required_field_errors(login_page):
    login_page.navigate()
    login_page.click(login_page.LOGIN_BUTTON)

    assert login_page.has_required_field_errors(), (
        "Expected 'Required' validation messages for empty Username/Password"
    )
