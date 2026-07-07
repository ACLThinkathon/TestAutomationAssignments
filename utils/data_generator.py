"""Random test-data generation so tests never collide on unique fields
(e.g. Username) and can be re-run repeatedly without manual cleanup.
"""
import string
from dataclasses import dataclass

from faker import Faker

fake = Faker()


@dataclass
class NewUserData:
    username: str
    password: str
    user_role: str
    status: str
    employee_search_term: str


def _random_suffix(length: int = 6) -> str:
    return "".join(fake.random_choices(elements=string.ascii_lowercase + string.digits, length=length))


def generate_username(prefix: str = "autouser") -> str:
    return f"{prefix}_{_random_suffix()}"


def generate_strong_password() -> str:
    # Guarantees upper, lower, digit and symbol to satisfy OrangeHRM's
    # password strength expectations.
    return f"Aa1!{_random_suffix(8)}"


def generate_new_user_data(
    user_role: str = "ESS",
    status: str = "Enabled",
    employee_search_term: str = "a",
    username_prefix: str = "autouser",
) -> NewUserData:
    """Builds a full data set for the "Add User" form.

    `employee_search_term` is intentionally a broad, single letter by
    default so the Employee Name autocomplete reliably returns at least
    one suggestion regardless of which employees currently exist in the
    shared demo environment.
    """
    return NewUserData(
        username=generate_username(username_prefix),
        password=generate_strong_password(),
        user_role=user_role,
        status=status,
        employee_search_term=employee_search_term,
    )
