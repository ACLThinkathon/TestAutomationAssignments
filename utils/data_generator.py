"""Random test-data generation so tests never collide on unique fields
(e.g. Username) and can be re-run repeatedly without manual cleanup.
"""
import random
import string
from dataclasses import dataclass
from datetime import date, timedelta

from faker import Faker

fake = Faker()


@dataclass
class NewUserData:
    username: str
    password: str
    user_role: str
    status: str
    employee_search_term: str


@dataclass
class NewEmployeeData:
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


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


def generate_employee_data(prefix: str = "AutoEmp") -> NewEmployeeData:
    """Builds a unique (first name, last name) pair for the PIM "Add
    Employee" form, so the same employee record can be reliably re-found by
    name in the Employee List afterwards.
    """
    return NewEmployeeData(first_name=prefix, last_name=_random_suffix())


def generate_random_word(length: int = 8) -> str:
    return _random_suffix(length)


@dataclass
class LeaveDates:
    date_str: str  # "yyyy-dd-mm", matching OrangeHRM's Apply Leave date fields
    leave_period: str  # e.g. "2026-01-01 - 2026-31-12", matching the Leave Period dropdown


def generate_leave_dates(min_days_ahead: int = 1, max_days_ahead: int = 460) -> LeaveDates:
    """Picks a random future date for an Apply Leave request.

    Randomizing (rather than a fixed offset) lets the test be re-run
    repeatedly without colliding with a leave request it already applied
    for on an earlier run -- OrangeHRM rejects a duplicate application for
    a date that already has one.
    """
    target = date.today() + timedelta(days=random.randint(min_days_ahead, max_days_ahead))
    return LeaveDates(
        date_str=target.strftime("%Y-%d-%m"),
        leave_period=f"{target.year}-01-01 - {target.year}-31-12",
    )
