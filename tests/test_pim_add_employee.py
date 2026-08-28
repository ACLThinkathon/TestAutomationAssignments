"""Add Employee scenario for PIM > Employee List."""
import allure
import pytest

from utils.data_generator import generate_employee_data

pytestmark = allure.feature("PIM")


@allure.story("Add Employee")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Adding a new employee makes them searchable in the Employee List")
@pytest.mark.smoke
def test_add_new_employee_successfully(pim_add_employee_page, employee_list_page):
    employee_data = generate_employee_data()

    pim_add_employee_page.navigate()
    pim_add_employee_page.add_employee(employee_data.first_name, employee_data.last_name)

    assert pim_add_employee_page.is_saved(), "Expected to be redirected to the new employee's Personal Details page"

    employee_list_page.navigate()
    employee_list_page.search_by_employee_name(employee_data.full_name)

    assert employee_list_page.is_employee_listed(employee_data.last_name), (
        f"Newly added employee '{employee_data.full_name}' was not found in the Employee List"
    )
