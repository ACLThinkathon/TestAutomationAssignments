# OrangeHRM UI Automation Framework

A Python + Playwright UI test automation framework built around the **Page
Object Model (POM)**, targeting the OrangeHRM demo site:
https://opensource-demo.orangehrmlive.com/

It ships with a working end-to-end scenario — **adding a new system user**
via Admin > User Management > Users > Add — and is structured so new page
objects and test cases can be added with minimal effort.

## Project structure

```
Orangehrm/
├── config/
│   └── config.py          # Env-driven configuration (URLs, credentials, timeouts)
├── pages/
│   ├── base_page.py        # Shared Playwright helpers used by every page object
│   ├── login_page.py       # Login screen
│   ├── dashboard_page.py   # Post-login dashboard / top navigation
│   ├── admin_users_page.py # Admin > User Management > Users (list/search)
│   └── add_user_page.py    # Admin > User Management > Users > Add (form)
├── utils/
│   └── data_generator.py   # Random/unique test data (Faker-based)
├── tests/
│   ├── conftest.py         # Fixtures: page objects + authenticated session
│   └── test_add_user.py    # Add User scenarios (happy path + negative)
├── requirements.txt
├── pytest.ini
├── .env.example
└── reports/                # HTML report output (generated)
```

## How the framework fits together

1. **`BasePage`** wraps the Playwright `Page` object with reusable
   primitives (`click`, `fill`, `select_oxd_dropdown_option`,
   `select_autocomplete_option`, `wait_for_toast`, ...). Every page object
   inherits from it.
2. **Page objects** (`pages/*.py`) expose only business-meaningful methods
   (e.g. `add_user_page.add_user(...)`, `admin_users_page.search_by_username(...)`).
   Locators live exclusively inside the page object that owns them.
3. **Fixtures** (`tests/conftest.py`) wire pages together and provide a
   ready-to-use, already-authenticated `page` (`logged_in_page`) plus one
   fixture per page object (`admin_users_page`, `add_user_page`, ...), so
   tests never touch Playwright APIs directly.
4. **Test data** (`utils/data_generator.py`) generates unique
   usernames/passwords per run using Faker, so tests are safe to re-run
   against the shared public demo instance without collisions.
5. **Configuration** (`config/config.py`) reads the base URL and
   credentials from environment variables / `.env`, defaulting to the
   public demo instance and its published `Admin` / `admin123` credentials.

## Setup

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browser binaries
playwright install chromium

# 4. (Optional) copy env file if you need to point at a different environment
cp .env.example .env
```

## Running the tests

```bash
# Run the full suite (headless, chromium)
pytest

# Run only smoke tests
pytest -m smoke

# Run headed, in slow motion, for debugging
pytest --headed --slowmo 300

# Run a specific test
pytest tests/test_add_user.py::test_add_new_user_successfully

# Run on a different browser
pytest --browser firefox
```

An HTML report is generated at `reports/report.html` after every run.
On failure, a screenshot, video, and Playwright trace are saved under
`test-results/` (open a trace with `playwright show-trace <trace.zip>`).

## Included scenario: Add New User

`tests/test_add_user.py` covers:

- **`test_add_new_user_successfully`** — logs in as Admin, navigates to
  Admin > User Management > Users, adds a new user with a random User
  Role/Employee/Status/Username/Password, verifies the success toast, then
  searches the Users list to confirm the new user appears.
- **`test_add_user_with_duplicate_username_shows_error`** — creates a
  user, then attempts to create a second user with the same username and
  asserts a validation error is shown.

## Adding new test cases

This framework is intentionally set up so growing the suite is
straightforward:

1. **New page?** Add a `pages/<name>_page.py` class inheriting from
   `BasePage`, define its locators as class constants, and expose
   business-level methods.
2. **New fixture?** Add it to `tests/conftest.py` (most new page objects
   only need `def my_page(logged_in_page): return MyPage(logged_in_page)`).
3. **New test?** Add a `tests/test_*.py` file, request the fixtures you
   need, and keep the test body to "arrange test data → call page object
   methods → assert".
