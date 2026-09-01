import allure
import pytest

from config.config import BASE_URL
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.data_generator import generate_new_user_data
from test_script_helpers import _run_genai_validation

pytestmark = allure.feature("Recorded Flow")


@allure.story("Recorded Flow")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Recorded OrangeHRM flow with search and logout")
@pytest.mark.smoke
def test_recorded_flow(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    page.goto(f"{BASE_URL}/web/index.php/auth/login", wait_until="domcontentloaded")
    page.get_by_placeholder("Username").first.fill("Admin")
    page.get_by_placeholder("Password").first.fill("admin123")
    page.get_by_role("button", name="Login").first.click(force=True)
    page.get_by_role("link", name="PIM", exact=True).first.click(force=True)
    page.get_by_placeholder("Type for hints...").first.fill("test")
    page.get_by_role("button", name="Search").first.click(force=True)
    _run_genai_validation(page, 'Verify search results show "test" text')
    page.get_by_text("ali user", exact=False).first.click(force=True)
    page.get_by_role("menuitem", name="Logout", exact=True).first.click(force=True)