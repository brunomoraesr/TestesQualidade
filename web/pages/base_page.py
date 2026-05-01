from typing import List, Tuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """
    Classe base para todos os Page Objects.
    Centraliza interações com o Selenium para que as subclasses
    trabalhem apenas com ações e verificações de negócio.
    """

    _TIMEOUT = 20  # 20s para absorver lentidão de runners de CI

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, self._TIMEOUT)

    # ── Localização ────────────────────────────────────────────────────────────

    def _find(self, locator: Tuple[str, str]) -> WebElement:
        """Aguarda o elemento ficar visível e o retorna."""
        return self._wait.until(EC.visibility_of_element_located(locator))

    def _find_clickable(self, locator: Tuple[str, str]) -> WebElement:
        """Aguarda o elemento ficar clicável e o retorna."""
        return self._wait.until(EC.element_to_be_clickable(locator))

    def _find_all(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Retorna todos os elementos encontrados; retorna [] se nenhum existir."""
        try:
            self._wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            return []
        return self._driver.find_elements(*locator)

    def _is_visible(self, locator: Tuple[str, str]) -> bool:
        try:
            return self._find(locator).is_displayed()
        except TimeoutException:
            return False

    # ── Ações ──────────────────────────────────────────────────────────────────

    def _click(self, locator: Tuple[str, str]) -> None:
        self._find_clickable(locator).click()

    def _fill(self, locator: Tuple[str, str], text: str) -> None:
        element = self._find(locator)
        element.clear()
        element.send_keys(text)

    def _select_by_value(self, locator: Tuple[str, str], value: str) -> None:
        from selenium.webdriver.support.ui import Select
        Select(self._find(locator)).select_by_value(value)

    # ── Leitura ────────────────────────────────────────────────────────────────

    def _text(self, locator: Tuple[str, str]) -> str:
        return self._find(locator).text.strip()

    def _texts(self, locator: Tuple[str, str]) -> List[str]:
        return [el.text.strip() for el in self._find_all(locator)]

    # ── Navegação ──────────────────────────────────────────────────────────────

    def navigate_to(self, url: str) -> None:
        self._driver.get(url)

    def _wait_for_url_contains(self, fragment: str) -> None:
        self._wait.until(EC.url_contains(fragment))

    @property
    def current_url(self) -> str:
        return self._driver.current_url

    @property
    def page_title(self) -> str:
        return self._driver.title
