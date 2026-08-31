"""Update My Info scenario for the logged-in user's own Personal Details."""
import allure
import pytest

from utils.data_generator import generate_random_word

pytestmark = allure.feature("My Info")


@allure.story("Update Personal Details")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Updated middle name persists after a page reload")
@pytest.mark.regression
def test_update_my_info_middle_name_persists(my_info_page):
    new_middle_name = generate_random_word()

    my_info_page.navigate()
    my_info_page.update_middle_name(new_middle_name)

    assert my_info_page.is_success_toast_visible(), "Expected a success toast after saving Personal Details"

    my_info_page.page.reload(wait_until="load")
    my_info_page.page.wait_for_load_state("networkidle")

    assert my_info_page.get_middle_name() == new_middle_name, (
        "Updated middle name was not persisted after reloading the page"
    )
