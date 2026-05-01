from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from web.pages.base_page import BasePage


class Header(BasePage):
    """
    Componente de cabeçalho presente em todas as páginas pós-login.
    Encapsula o menu lateral (hamburguer) e o ícone do carrinho.
    """

    _CART_ICON       = (By.CLASS_NAME, "shopping_cart_link")
    _CART_BADGE      = (By.CLASS_NAME, "shopping_cart_badge")
    _PAGE_TITLE      = (By.CLASS_NAME, "title")
    _MENU_BUTTON     = (By.ID, "react-burger-menu-btn")
    _LOGOUT_LINK     = (By.ID, "logout_sidebar_link")
    _RESET_LINK      = (By.ID, "reset_sidebar_link")
    _ALL_ITEMS_LINK  = (By.ID, "inventory_sidebar_link")
    _CLOSE_MENU_BTN  = (By.ID, "react-burger-cross-btn")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    # ── Carrinho ───────────────────────────────────────────────────────────────

    def go_to_cart(self) -> None:
        self._click(self._CART_ICON)
        self._wait_for_url_contains("cart.html")

    @property
    def cart_item_count(self) -> int:
        """Retorna o número no badge do carrinho; 0 se o badge não existir."""
        if not self._is_visible(self._CART_BADGE):
            return 0
        return int(self._text(self._CART_BADGE))

    @property
    def cart_badge_is_visible(self) -> bool:
        return self._is_visible(self._CART_BADGE)

    # ── Menu lateral ───────────────────────────────────────────────────────────

    def open_menu(self) -> None:
        self._click(self._MENU_BUTTON)
        self._find(self._LOGOUT_LINK)

    def close_menu(self) -> None:
        self._click(self._CLOSE_MENU_BTN)

    def logout(self) -> None:
        self.open_menu()
        self._click(self._LOGOUT_LINK)
        self._wait_for_url_contains("index.html")

    def reset_app_state(self) -> None:
        """Limpa o carrinho e reseta o estado da aplicação via menu."""
        self.open_menu()
        self._click(self._RESET_LINK)
        self.close_menu()

    def go_to_all_items(self) -> None:
        self.open_menu()
        self._click(self._ALL_ITEMS_LINK)
        self._wait_for_url_contains("inventory.html")

    # ── Título da página ───────────────────────────────────────────────────────

    @property
    def page_header_text(self) -> str:
        return self._text(self._PAGE_TITLE)
