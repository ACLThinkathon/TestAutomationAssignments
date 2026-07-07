"""Base class for all Page Objects.

Every concrete page (LoginPage, DashboardPage, ...) inherits from BasePage
and gets a small, consistent toolkit for interacting with the Playwright
`Page` object. Centralizing these primitives here means:
  * locator strategy / waits are consistent across the whole framework
  * if Playwright's API changes, only this file needs updating
  * new page objects stay short and focused on "what", not "how"
"""
from __future__ import annotations

from playwright.sync_api import Page

from config.config import Config


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = Config.DEFAULT_TIMEOUT_MS

    # --- navigation -----------------------------------------------------
    def goto(self, url: str) -> None:
        self.page.goto(url, wait_until="load")

    def current_url(self) -> str:
        return self.page.url

    # --- element interaction ---------------------------------------------
    def click(self, selector: str) -> None:
        self.page.locator(selector).first.click(timeout=self.timeout)

    def fill(self, selector: str, text: str) -> None:
        locator = self.page.locator(selector).first
        locator.wait_for(state="visible", timeout=self.timeout)
        locator.fill(text, timeout=self.timeout)

    def type_text(self, selector: str, text: str, delay: int = 50) -> None:
        self.page.locator(selector).first.type(text, delay=delay, timeout=self.timeout)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).first.inner_text(timeout=self.timeout)

    def is_visible(self, selector: str, timeout: int | None = None) -> bool:
        try:
            self.page.locator(selector).first.wait_for(
                state="visible", timeout=timeout or self.timeout
            )
            return True
        except Exception:
            return False

    def count(self, selector: str) -> int:
        return self.page.locator(selector).count()

    # --- custom OrangeHRM (oxd) widgets ----------------------------------
    def select_oxd_dropdown_option(self, dropdown_selector: str, option_text: str) -> None:
        """Handles OrangeHRM's custom (non-native) `<select>` replacement.

        Clicking the dropdown reveals a floating list of
        `div.oxd-select-option` items; we then click the one matching
        `option_text`.
        """
        self.page.locator(dropdown_selector).first.click(timeout=self.timeout)
        option = self.page.locator("div.oxd-select-option", has_text=option_text).first
        option.wait_for(state="visible", timeout=self.timeout)
        option.click(timeout=self.timeout)

    def select_autocomplete_option(self, input_selector: str, search_term: str) -> str:
        """Types into an OrangeHRM autocomplete input and picks the first
        real suggestion. Returns the text of the option that was selected.

        While results are loading, OrangeHRM briefly renders a
        "Searching...." placeholder using the same option class, so we
        explicitly wait for a genuine option (i.e. one whose text is not
        that placeholder) before clicking to avoid selecting it by mistake.
        """
        field = self.page.locator(input_selector).first
        field.click(timeout=self.timeout)
        field.fill(search_term, timeout=self.timeout)
        option = self.page.locator(
            "div.oxd-autocomplete-option:not(:has-text('Searching'))"
        ).first
        option.wait_for(state="visible", timeout=self.timeout)
        selected_text = option.inner_text()
        option.click(timeout=self.timeout)
        return selected_text

    def wait_for_toast(self, timeout: int | None = None) -> str:
        toast = self.page.locator(".oxd-toast")
        toast.first.wait_for(state="visible", timeout=timeout or self.timeout)
        return toast.first.inner_text()
