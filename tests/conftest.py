"""Shared pytest fixtures.

These build on top of pytest-playwright's built-in `page` fixture (which
already gives each test a fresh browser page/context) and layer the Page
Object Model on top, plus a ready-to-use authenticated session so
individual tests stay focused on behaviour, not setup boilerplate.
"""
from pathlib import Path

import allure
import pytest

from config.config import Config
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_users_page import AdminUsersPage
from pages.add_user_page import AddUserPage
from pages.pim_add_employee_page import PimAddEmployeePage
from pages.employee_list_page import EmployeeListPage
from pages.my_info_page import MyInfoPage


@pytest.fixture
def browser_context_args(browser_context_args):
    """Overrides pytest-playwright's default context args."""
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "ignore_https_errors": True,
    }


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page):
    return DashboardPage(page)


@pytest.fixture
def logged_in_page(page, login_page):
    """Logs in as the configured admin user and returns the raw Page,
    already parked on the Dashboard.
    """
    login_page.navigate()
    login_page.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)
    DashboardPage(page).is_loaded()
    return page


@pytest.fixture
def admin_users_page(logged_in_page):
    return AdminUsersPage(logged_in_page)


@pytest.fixture
def add_user_page(logged_in_page):
    return AddUserPage(logged_in_page)


@pytest.fixture
def pim_add_employee_page(logged_in_page):
    return PimAddEmployeePage(logged_in_page)


@pytest.fixture
def employee_list_page(logged_in_page):
    return EmployeeListPage(logged_in_page)


@pytest.fixture
def my_info_page(logged_in_page):
    return MyInfoPage(logged_in_page)


def pytest_sessionstart(session):
    """Writes environment.properties into the Allure results dir so the
    generated report's Environment tab shows what this run targeted.
    """
    alluredir = session.config.getoption("allure_report_dir", default=None)
    if not alluredir:
        return
    Path(alluredir).mkdir(parents=True, exist_ok=True)
    browsers = session.config.getoption("browser", default=None) or ["chromium"]
    properties = {
        "Base.URL": Config.BASE_URL,
        "Browser": ", ".join(browsers),
    }
    content = "\n".join(f"{key}={value}" for key, value in properties.items())
    (Path(alluredir) / "environment.properties").write_text(content, encoding="utf-8")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Exposes each phase's outcome as item.rep_<phase> so fixtures (below)
    can tell whether the test itself failed.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def attach_screenshot_on_failure(request, page):
    """Attaches a full-page screenshot to the Allure report for any test
    that fails, so a failure can be triaged from the report alone.
    """
    yield
    if getattr(request.node, "rep_call", None) is not None and request.node.rep_call.failed:
        try:
            allure.attach(
                page.screenshot(full_page=True),
                name="failure-screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception:
            pass
