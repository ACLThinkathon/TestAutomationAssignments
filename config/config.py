"""Central place for environment-driven configuration.

All values can be overridden via environment variables or a local .env file
(see .env.example). Keeping configuration here means page objects and tests
never hardcode URLs or credentials.
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL: str = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com").rstrip("/")

    ADMIN_USERNAME: str = os.getenv("ORANGEHRM_USERNAME", "Admin")
    ADMIN_PASSWORD: str = os.getenv("ORANGEHRM_PASSWORD", "admin123")

    DEFAULT_TIMEOUT_MS: int = int(os.getenv("DEFAULT_TIMEOUT_MS", "15000"))

    LOGIN_URL: str = f"{BASE_URL}/web/index.php/auth/login"
    DASHBOARD_URL: str = f"{BASE_URL}/web/index.php/dashboard/index"
    ADD_USER_URL: str = f"{BASE_URL}/web/index.php/admin/saveSystemUser"
    SYSTEM_USERS_URL: str = f"{BASE_URL}/web/index.php/admin/viewSystemUsers"
