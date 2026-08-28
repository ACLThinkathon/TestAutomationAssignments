"""Search scenarios for Admin > User Management > Users."""
import allure
import pytest

from config.config import Config

pytestmark = allure.feature("Admin User Management")


@allure.story("Search Users")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Searching an existing username returns that user")
@pytest.mark.smoke
def test_search_existing_user_returns_result(admin_users_page):
    admin_users_page.navigate()
    admin_users_page.search_by_username(Config.ADMIN_USERNAME)

    assert admin_users_page.is_user_listed(Config.ADMIN_USERNAME), (
        f"Expected '{Config.ADMIN_USERNAME}' to appear in the search results"
    )


@allure.story("Search Users")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Searching a nonexistent username returns no results")
@pytest.mark.regression
@pytest.mark.negative
def test_search_nonexistent_user_returns_no_results(admin_users_page):
    admin_users_page.navigate()
    admin_users_page.search_by_username("no_such_user_zzz_999")

    assert admin_users_page.has_no_results(), "Expected no rows for a username that does not exist"


@allure.story("Search Users")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Reset clears the search filter and shows the full list")
@pytest.mark.regression
def test_reset_clears_search_filter(admin_users_page):
    admin_users_page.navigate()
    admin_users_page.search_by_username(Config.ADMIN_USERNAME)
    assert admin_users_page.is_any_result_visible()

    admin_users_page.click_reset()

    assert admin_users_page.get_username_filter_value() == "", "Expected the Username filter to be cleared after Reset"
    assert admin_users_page.is_any_result_visible(), "Expected the full user list to be shown again after Reset"
