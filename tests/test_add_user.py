"""Add User scenarios for Admin > User Management.

These tests demonstrate the intended usage pattern for this framework:
compose page objects (via fixtures), generate isolated test data, and
assert on outcomes only, keeping test bodies short and readable.
"""
import pytest

from utils.data_generator import generate_new_user_data


@pytest.mark.smoke
def test_add_new_user_successfully(admin_users_page, add_user_page):
    user_data = generate_new_user_data(user_role="ESS", status="Enabled")

    admin_users_page.navigate()
    admin_users_page.click_add()

    add_user_page.add_user(
        user_role=user_data.user_role,
        employee_search_term=user_data.employee_search_term,
        status=user_data.status,
        username=user_data.username,
        password=user_data.password,
    )

    assert add_user_page.is_success_toast_visible(), "Expected a success toast after saving the new user"

    admin_users_page.navigate()
    admin_users_page.search_by_username(user_data.username)

    assert admin_users_page.is_user_listed(user_data.username), (
        f"Newly created user '{user_data.username}' was not found in the Users list"
    )


@pytest.mark.regression
@pytest.mark.negative
def test_add_user_with_duplicate_username_shows_error(admin_users_page, add_user_page):
    user_data = generate_new_user_data(user_role="ESS", status="Enabled")

    # Create the user once.
    admin_users_page.navigate()
    admin_users_page.click_add()
    add_user_page.add_user(
        user_role=user_data.user_role,
        employee_search_term=user_data.employee_search_term,
        status=user_data.status,
        username=user_data.username,
        password=user_data.password,
    )
    assert add_user_page.is_success_toast_visible()

    # Attempt to create a second user with the same username.
    admin_users_page.navigate()
    admin_users_page.click_add()
    add_user_page.add_user(
        user_role=user_data.user_role,
        employee_search_term=user_data.employee_search_term,
        status=user_data.status,
        username=user_data.username,
        password=user_data.password,
    )

    assert add_user_page.has_field_error(), "Expected a validation error for the duplicate username"
