"""Apply Leave scenario for Leave > Apply / My Leave."""
import allure
import pytest

from utils.data_generator import generate_leave_dates

pytestmark = allure.feature("Leave")

LEAVE_TYPE = "US - Vacation"


@allure.story("Apply Leave")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Applying for leave succeeds and appears under My Leave as Pending Approval")
@pytest.mark.smoke
def test_apply_leave_appears_as_pending_approval(
    my_info_page, leave_entitlement_page, apply_leave_page, my_leave_page
):
    employee_name = my_info_page.navigate().get_full_name()
    leave_dates = generate_leave_dates()

    # Arrange: OrangeHRM only lists leave types with an existing balance on
    # the Apply Leave form, so grant one for the logged-in employee first.
    leave_entitlement_page.navigate()
    leave_entitlement_page.add_entitlement(employee_name, LEAVE_TYPE, leave_dates.leave_period, "5")

    apply_leave_page.navigate()
    apply_leave_page.apply_leave(LEAVE_TYPE, leave_dates.date_str, leave_dates.date_str)

    assert apply_leave_page.is_success_toast_visible(), "Expected a success confirmation after applying for leave"

    my_leave_page.navigate()
    assert my_leave_page.has_pending_approval_request(leave_dates.date_str), (
        f"Expected the leave request on {leave_dates.date_str} to appear under My Leave with status 'Pending Approval'"
    )


import allure
import pytest

from utils.data_generator import generate_leave_dates

pytestmark = allure.feature("Leave")

LEAVE_TYPE = "US - Vacation"


@allure.story("Apply Leave")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Applying for leave succeeds and appears under My Leave as Pending Approval")
@pytest.mark.smoke
def test_apply_leave_appears_as_pending_approval(
    my_info_page, leave_entitlement_page, apply_leave_page, my_leave_page, dashboard_page
):
    employee_name = my_info_page.navigate().get_full_name()
    leave_dates = generate_leave_dates()

    # Arrange: OrangeHRM only lists leave types with an existing balance on
    # the Apply Leave form, so grant one for the logged-in employee first.
    leave_entitlement_page.navigate()
    leave_entitlement_page.add_entitlement(employee_name, LEAVE_TYPE, leave_dates.leave_period, "5")

    apply_leave_page.navigate()
    apply_leave_page.apply_leave(LEAVE_TYPE, leave_dates.date_str, leave_dates.date_str)

    assert apply_leave_page.is_success_toast_visible(), "Expected a success confirmation after applying for leave"

    my_leave_page.navigate()
    assert my_leave_page.has_pending_approval_request(leave_dates.date_str), (
        f"Expected the leave request on {leave_dates.date_str} to appear under My Leave with status 'Pending Approval'"
    )

    dashboard_page.logout()
