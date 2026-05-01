"""
Page Objects do fluxo de checkout do SauceDemo.

Três páginas em sequência:
    CheckoutStepOnePage   → /checkout-step-one.html  (dados do comprador)
    CheckoutStepTwoPage   → /checkout-step-two.html  (resumo do pedido)
    CheckoutCompletePage  → /checkout-complete.html  (confirmação)
"""

from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from web.components.header import Header
from web.pages.base_page import BasePage


# ── Step 1: Dados do comprador ─────────────────────────────────────────────────

class CheckoutStepOnePage(BasePage):
    """
    Page Object para /checkout-step-one.html
    Coleta first name, last name e ZIP code do comprador.
    """

    URL = "https://www.saucedemo.com/checkout-step-one.html"

    _FIRST_NAME_INPUT = (By.CSS_SELECTOR, "[data-test='firstName']")
    _LAST_NAME_INPUT  = (By.CSS_SELECTOR, "[data-test='lastName']")
    _ZIP_CODE_INPUT   = (By.CSS_SELECTOR, "[data-test='postalCode']")
    _CONTINUE_BUTTON  = (By.CSS_SELECTOR, "[data-test='continue']")
    _CANCEL_BUTTON    = (By.CSS_SELECTOR, "[data-test='cancel']")
    _ERROR_MESSAGE    = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.header = Header(driver)

    # ── Ações ──────────────────────────────────────────────────────────────────

    def enter_first_name(self, value: str) -> "CheckoutStepOnePage":
        self._fill(self._FIRST_NAME_INPUT, value)
        return self

    def enter_last_name(self, value: str) -> "CheckoutStepOnePage":
        self._fill(self._LAST_NAME_INPUT, value)
        return self

    def enter_zip_code(self, value: str) -> "CheckoutStepOnePage":
        self._fill(self._ZIP_CODE_INPUT, value)
        return self

    def fill_buyer_info(self, first_name: str, last_name: str, zip_code: str) -> "CheckoutStepOnePage":
        """Método conveniente: preenche todos os campos de uma vez."""
        return (
            self.enter_first_name(first_name)
                .enter_last_name(last_name)
                .enter_zip_code(zip_code)
        )

    def click_continue(self) -> None:
        self._click(self._CONTINUE_BUTTON)
        self._wait_for_url_contains("checkout-step-two.html")

    def click_cancel(self) -> None:
        self._click(self._CANCEL_BUTTON)
        self._wait_for_url_contains("cart.html")

    # ── Verificações ───────────────────────────────────────────────────────────

    @property
    def error_message(self) -> str:
        return self._text(self._ERROR_MESSAGE)

    @property
    def has_error(self) -> bool:
        return self._is_visible(self._ERROR_MESSAGE)

    @property
    def is_on_page(self) -> bool:
        return self._is_visible(self._CONTINUE_BUTTON)


# ── Step 2: Resumo do pedido ───────────────────────────────────────────────────

class CheckoutStepTwoPage(BasePage):
    """
    Page Object para /checkout-step-two.html
    Exibe o resumo do pedido com itens, subtotal, imposto e total.
    """

    URL = "https://www.saucedemo.com/checkout-step-two.html"

    _CART_ITEMS         = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES         = (By.CLASS_NAME, "inventory_item_name")
    _ITEM_PRICES        = (By.CLASS_NAME, "inventory_item_price")
    _SUBTOTAL_LABEL     = (By.CLASS_NAME, "summary_subtotal_label")
    _TAX_LABEL          = (By.CLASS_NAME, "summary_tax_label")
    _TOTAL_LABEL        = (By.CLASS_NAME, "summary_total_label")
    _FINISH_BUTTON      = (By.CSS_SELECTOR, "[data-test='finish']")
    _CANCEL_BUTTON      = (By.CSS_SELECTOR, "[data-test='cancel']")
    _PAYMENT_INFO       = (By.CLASS_NAME, "summary_value_label")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.header = Header(driver)

    # ── Ações ──────────────────────────────────────────────────────────────────

    def click_finish(self) -> None:
        self._click(self._FINISH_BUTTON)
        self._wait_for_url_contains("checkout-complete.html")

    def click_cancel(self) -> None:
        self._click(self._CANCEL_BUTTON)
        self._wait_for_url_contains("inventory.html")

    # ── Leitura do resumo ──────────────────────────────────────────────────────

    @property
    def item_names(self) -> List[str]:
        return self._texts(self._ITEM_NAMES)

    @property
    def item_prices(self) -> List[float]:
        raw = self._texts(self._ITEM_PRICES)
        return [float(p.replace("$", "")) for p in raw]

    @property
    def item_count(self) -> int:
        return len(self._find_all(self._CART_ITEMS))

    def _parse_currency(self, locator) -> float:
        raw = self._text(locator)
        # Ex.: "Item total: $29.99"  →  29.99
        return float(raw.split("$")[-1])

    @property
    def subtotal(self) -> float:
        return self._parse_currency(self._SUBTOTAL_LABEL)

    @property
    def tax(self) -> float:
        return self._parse_currency(self._TAX_LABEL)

    @property
    def total(self) -> float:
        return self._parse_currency(self._TOTAL_LABEL)

    @property
    def total_matches_subtotal_plus_tax(self) -> bool:
        return round(self.subtotal + self.tax, 2) == round(self.total, 2)

    # ── Verificações ───────────────────────────────────────────────────────────

    @property
    def is_on_page(self) -> bool:
        return self._is_visible(self._FINISH_BUTTON)


# ── Step 3: Confirmação ────────────────────────────────────────────────────────

class CheckoutCompletePage(BasePage):
    """
    Page Object para /checkout-complete.html
    Exibe a mensagem de confirmação após finalizar a compra.
    """

    URL = "https://www.saucedemo.com/checkout-complete.html"

    _COMPLETE_HEADER  = (By.CLASS_NAME, "complete-header")
    _COMPLETE_TEXT    = (By.CLASS_NAME, "complete-text")
    _BACK_HOME_BUTTON = (By.CSS_SELECTOR, "[data-test='back-to-products']")
    _PONY_IMAGE       = (By.CLASS_NAME, "pony_express")

    EXPECTED_HEADER = "Thank you for your order!"
    EXPECTED_TEXT   = "Your order has been dispatched"

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    # ── Ações ──────────────────────────────────────────────────────────────────

    def go_back_to_products(self) -> None:
        self._click(self._BACK_HOME_BUTTON)
        self._wait_for_url_contains("inventory.html")

    # ── Verificações ───────────────────────────────────────────────────────────

    @property
    def confirmation_header(self) -> str:
        return self._text(self._COMPLETE_HEADER)

    @property
    def confirmation_text(self) -> str:
        return self._text(self._COMPLETE_TEXT)

    @property
    def order_confirmed(self) -> bool:
        return self.EXPECTED_HEADER in self.confirmation_header

    @property
    def pony_image_displayed(self) -> bool:
        return self._is_visible(self._PONY_IMAGE)

    @property
    def is_on_page(self) -> bool:
        return self._is_visible(self._COMPLETE_HEADER)
