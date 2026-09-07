"""End-to-end scenario spanning Admin, ESS (self-service), and Admin again:
create an employee and a linked user account, have that user log in and
update their own Personal Details, then confirm Admin sees the change.
"""
import allure
import pytest

from config.config import Config
from pages.login_page import LoginPage
from pages.my_info_page import MyInfoPage
from utils.data_generator import generate_employee_data, generate_new_user_data, generate_random_word

pytestmark = allure.feature("Employee Lifecycle")


@allure.story("Create Employee, Self-Service Update, Admin Verification")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("A newly created employee's user can log in, update their own info, and Admin sees the change")
@pytest.mark.smoke
def test_new_employee_user_updates_own_profile_and_admin_verifies(
    pim_add_employee_page,
    employee_list_page,
    admin_users_page,
    add_user_page,
    dashboard_page,
    page,
):
    employee_data = generate_employee_data()
    user_data = generate_new_user_data(user_role="Admin", status="Enabled")
    new_middle_name = generate_random_word()

    # Step 2: create the employee, then a system user (Admin role) linked to it.
    pim_add_employee_page.navigate()
    pim_add_employee_page.add_employee(employee_data.first_name, employee_data.last_name)
    assert pim_add_employee_page.is_saved(), "Expected the new employee record to be saved"

    admin_users_page.navigate()
    admin_users_page.click_add()
    add_user_page.add_user(
        user_role=user_data.user_role,
        employee_search_term=employee_data.full_name,
        status=user_data.status,
        username=user_data.username,
        password=user_data.password,
    )
    assert add_user_page.is_success_toast_visible(), "Expected End User created successfully"

    # Step 3: search and verify the user was created.
    admin_users_page.navigate()
    admin_users_page.search_by_username(user_data.username)
    assert admin_users_page.is_user_listed(user_data.username), "Expected End User searched successfully"

    # Step 4: log in as the new user and update their own Personal Details.
    dashboard_page.logout()

    login_page = LoginPage(page)
    login_page.login(user_data.username, user_data.password)
    assert dashboard_page.is_loaded(), "Expected End User login successful"

    my_info_page = MyInfoPage(page)
    my_info_page.navigate()
    my_info_page.update_middle_name(new_middle_name)
    assert my_info_page.is_success_toast_visible(), "Expected End User info update successful"

    # Step 5: log out as the new user.
    dashboard_page.logout()

    # Step 6-7: log back in as admin and search for the user again.
    login_page.login(Config.ADMIN_USERNAME, Config.ADMIN_PASSWORD)
    assert dashboard_page.is_loaded(), "Expected admin login to succeed after logging back in"

    admin_users_page.navigate()
    admin_users_page.search_by_username(user_data.username)
    assert admin_users_page.is_user_listed(user_data.username), "Expected the user to still be listed for admin"

    # Step 8: validate the updated info is visible from the admin's view of the employee record.
    # Matched on last_name alone (not full_name): the ESS update above just
    # changed this same employee's middle name, so the Employee List's name
    # column no longer contains "first last" as a contiguous substring.
    employee_list_page.navigate()
    employee_list_page.search_by_employee_name(employee_data.full_name)
    employee_list_page.open_employee(employee_data.last_name)

    assert MyInfoPage(page).get_middle_name() == new_middle_name, (
        "Expected End User info updated in admin view"
    )
