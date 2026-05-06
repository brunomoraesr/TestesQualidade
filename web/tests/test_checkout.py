"""
Testes E2E — Checkout do SauceDemo.

Cenários cobertos:
    - Preencher formulário com campo obrigatório vazio exibe erro
    - Fluxo completo: login → produto → carrinho → checkout → confirmação
"""

import pytest

from web.pages.cart_page import CartPage
from web.pages.checkout_page import (
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)


PRODUCT = "Sauce Labs Backpack"


@pytest.mark.web
class TestCheckout:

    def test_fill_missing_field_shows_error(self, logged_in, users, driver):
        logged_in.add_to_cart(PRODUCT)
        logged_in.header.go_to_cart()
        CartPage(driver).proceed_to_checkout()

        info = users["checkout_info"]
        step_one = CheckoutStepOnePage(driver)
        step_one.fill_buyer_info("", info["last_name"], info["zip_code"])
        step_one.click_continue()

        assert "First Name is required" in step_one.error_message

    def test_complete_purchase(self, logged_in, users, driver):
        logged_in.add_to_cart(PRODUCT)
        logged_in.header.go_to_cart()
        CartPage(driver).proceed_to_checkout()

        info = users["checkout_info"]
        step_one = CheckoutStepOnePage(driver)
        step_one.fill_buyer_info(info["first_name"], info["last_name"], info["zip_code"])
        step_one.click_continue()

        CheckoutStepTwoPage(driver).click_finish()

        assert CheckoutCompletePage(driver).order_confirmed
