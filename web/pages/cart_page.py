from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from web.components.header import Header
from web.pages.base_page import BasePage


class CartPage(BasePage):
    """
    Page Object para https://www.saucedemo.com/cart.html
    Responsável pela visualização e gerenciamento do carrinho de compras.
    """

    URL = "https://www.saucedemo.com/cart.html"

    _CART_ITEMS          = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES          = (By.CLASS_NAME, "inventory_item_name")
    _ITEM_PRICES         = (By.CLASS_NAME, "inventory_item_price")
    _ITEM_QUANTITIES     = (By.CLASS_NAME, "cart_quantity")
    _CHECKOUT_BUTTON     = (By.CSS_SELECTOR, "[data-test='checkout']")
    _CONTINUE_SHOPPING   = (By.CSS_SELECTOR, "[data-test='continue-shopping']")
    _REMOVE_BUTTONS      = (By.CSS_SELECTOR, "[data-test^='remove']")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.header = Header(driver)

    # ── Navegação ──────────────────────────────────────────────────────────────

    def open(self) -> "CartPage":
        self.navigate_to(self.URL)
        return self

    def proceed_to_checkout(self) -> None:
        self._click(self._CHECKOUT_BUTTON)
        self._wait_for_url_contains("checkout-step-one.html")

    def continue_shopping(self) -> None:
        self._click(self._CONTINUE_SHOPPING)
        self._wait_for_url_contains("inventory.html")

    # ── Itens do carrinho ──────────────────────────────────────────────────────

    @property
    def item_names(self) -> List[str]:
        return self._texts(self._ITEM_NAMES)

    @property
    def item_prices(self) -> List[float]:
        raw = self._texts(self._ITEM_PRICES)
        return [float(p.replace("$", "")) for p in raw]

    @property
    def item_quantities(self) -> List[int]:
        return [int(q) for q in self._texts(self._ITEM_QUANTITIES)]

    @property
    def item_count(self) -> int:
        return len(self._find_all(self._CART_ITEMS))

    @property
    def is_empty(self) -> bool:
        return self.item_count == 0

    def contains_item(self, product_name: str) -> bool:
        return product_name in self.item_names

    def remove_item(self, product_name: str) -> "CartPage":
        slug = product_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        locator = (By.CSS_SELECTOR, f"[data-test='remove-{slug}']")
        self._click(locator)
        return self

    def remove_all_items(self) -> "CartPage":
        for button in self._find_all(self._REMOVE_BUTTONS):
            button.click()
        return self

    # ── Verificações ───────────────────────────────────────────────────────────

    @property
    def is_on_page(self) -> bool:
        return self._is_visible(self._CHECKOUT_BUTTON)
