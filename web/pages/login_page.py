from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from web.pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object para https://www.saucedemo.com/
    Responsável por todas as interações da tela de login.
    """

    URL = "https://www.saucedemo.com/"

    _USERNAME_INPUT  = (By.ID, "user-name")
    _PASSWORD_INPUT  = (By.ID, "password")
    _LOGIN_BUTTON    = (By.ID, "login-button")
    _ERROR_MESSAGE   = (By.CSS_SELECTOR, "[data-test='error']")
    _ERROR_BUTTON    = (By.CLASS_NAME, "error-button")
    _LOGO            = (By.CLASS_NAME, "login_logo")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    # ── Ações ──────────────────────────────────────────────────────────────────

    def open(self) -> "LoginPage":
        self.navigate_to(self.URL)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        self._fill(self._USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self._fill(self._PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        self._click(self._LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Método conveniente: preenche credenciais e submete o formulário."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def dismiss_error(self) -> "LoginPage":
        self._click(self._ERROR_BUTTON)
        return self

    # ── Verificações ───────────────────────────────────────────────────────────

    @property
    def error_message(self) -> str:
        return self._text(self._ERROR_MESSAGE)

    @property
    def has_error(self) -> bool:
        return self._is_visible(self._ERROR_MESSAGE)

    @property
    def is_on_page(self) -> bool:
        return self._is_visible(self._LOGIN_BUTTON)

    @property
    def logo_text(self) -> str:
        return self._text(self._LOGO)
