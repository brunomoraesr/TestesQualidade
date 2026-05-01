from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from web.components.header import Header
from web.pages.base_page import BasePage


class InventoryPage(BasePage):
    """
    Page Object para https://www.saucedemo.com/inventory.html
    Responsável pela listagem de produtos e interações com o carrinho.
    """

    URL = "https://www.saucedemo.com/inventory.html"

    _PRODUCT_LIST        = (By.CLASS_NAME, "inventory_list")
    _PRODUCT_ITEMS       = (By.CLASS_NAME, "inventory_item")
    _PRODUCT_NAMES       = (By.CLASS_NAME, "inventory_item_name")
    _PRODUCT_PRICES      = (By.CLASS_NAME, "inventory_item_price")
    _PRODUCT_DESC        = (By.CLASS_NAME, "inventory_item_desc")
    _ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    _REMOVE_BUTTONS      = (By.CSS_SELECTOR, "[data-test^='remove']")
    _SORT_DROPDOWN       = (By.CSS_SELECTOR, "[data-test='product_sort_container']")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.header = Header(driver)

    # ── Navegação ──────────────────────────────────────────────────────────────

    def open(self) -> "InventoryPage":
        self.navigate_to(self.URL)
        return self

    # ── Produtos ───────────────────────────────────────────────────────────────

    @property
    def product_names(self) -> List[str]:
        return self._texts(self._PRODUCT_NAMES)

    @property
    def product_prices(self) -> List[float]:
        raw = self._texts(self._PRODUCT_PRICES)
        return [float(p.replace("$", "")) for p in raw]

    @property
    def product_count(self) -> int:
        return len(self._find_all(self._PRODUCT_ITEMS))

    def _slug(self, product_name: str) -> str:
        """Converte nome do produto no slug usado pelos atributos data-test."""
        return product_name.lower().replace(" ", "-").replace("(", "").replace(")", "")

    def add_to_cart(self, product_name: str) -> "InventoryPage":
        """Adiciona um produto ao carrinho pelo nome exato exibido na página."""
        slug = self._slug(product_name)
        self._click((By.CSS_SELECTOR, f"[data-test='add-to-cart-{slug}']"))
        # Aguarda o botão mudar para "Remove", confirmando que o React terminou
        # de atualizar o estado antes de qualquer ação subsequente.
        self._find((By.CSS_SELECTOR, f"[data-test='remove-{slug}']"))
        return self

    def remove_from_cart(self, product_name: str) -> "InventoryPage":
        slug = self._slug(product_name)
        self._click((By.CSS_SELECTOR, f"[data-test='remove-{slug}']"))
        # Aguarda o botão voltar para "Add to cart", confirmando remoção.
        self._find((By.CSS_SELECTOR, f"[data-test='add-to-cart-{slug}']"))
        return self

    def add_all_to_cart(self) -> "InventoryPage":
        """Adiciona produto por produto re-buscando o seletor a cada iteração
        para evitar referências stale após mutação do DOM."""
        for name in self.product_names:
            self.add_to_cart(name)
        return self

    def open_product(self, product_name: str) -> None:
        locator = (By.LINK_TEXT, product_name)
        self._click(locator)
        self._wait_for_url_contains("inventory-item.html")

    # ── Ordenação ──────────────────────────────────────────────────────────────

    def sort_by(self, option: str) -> "InventoryPage":
        """
        Opções válidas: 'az' | 'za' | 'lohi' | 'hilo'
        (A→Z, Z→A, preço crescente, preço decrescente)
        """
        self._select_by_value(self._SORT_DROPDOWN, option)
        return self

    # ── Verificações ───────────────────────────────────────────────────────────

    @property
    def is_on_page(self) -> bool:
        return self._is_visible(self._PRODUCT_LIST)

    @property
    def cart_item_count(self) -> int:
        return self.header.cart_item_count
