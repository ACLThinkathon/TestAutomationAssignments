"""Shared pytest fixtures.

These build on top of pytest-playwright's built-in `page` fixture (which
already gives each test a fresh browser page/context) and layer the Page
Object Model on top, plus a ready-to-use authenticated session so
individual tests stay focused on behaviour, not setup boilerplate.
"""
import pytest

from config.config import Config
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.admin_users_page import AdminUsersPage
from pages.add_user_page import AddUserPage


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
