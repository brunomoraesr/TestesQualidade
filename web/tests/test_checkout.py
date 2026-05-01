"""
Testes E2E — Fluxo de checkout do SauceDemo.

Cenários cobertos:
    - Fluxo completo: login → 2 produtos → carrinho → checkout →
      preencher dados → finalizar → "Thank you for your order!"
    - Validações de campos obrigatórios no step 1
    - Resumo do pedido exibe itens e valores corretos
    - Total = subtotal + imposto
    - Cancelar no step 2 retorna ao inventário
    - Botão "Back Home" retorna ao inventário após confirmação
"""

import pytest

from web.pages.cart_page import CartPage
from web.pages.checkout_page import (
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)


PRODUCT_1 = "Sauce Labs Backpack"
PRODUCT_2 = "Sauce Labs Bike Light"


@pytest.mark.web
class TestCompleteCheckoutFlow:

    def test_full_purchase_flow_confirmation_message(self, logged_in, users, driver):
        """
        Fluxo completo E2E:
        login → adiciona 2 produtos → carrinho → checkout →
        preenche dados → finaliza → verifica "Thank you for your order!"
        """
        # 1. Adicionar 2 produtos ao carrinho
        logged_in.add_to_cart(PRODUCT_1)
        logged_in.add_to_cart(PRODUCT_2)
        assert logged_in.cart_item_count == 2

        # 2. Ir ao carrinho e verificar itens
        logged_in.header.go_to_cart()
        cart = CartPage(driver)
        assert cart.contains_item(PRODUCT_1)
        assert cart.contains_item(PRODUCT_2)

        # 3. Iniciar checkout
        cart.proceed_to_checkout()
        step_one = CheckoutStepOnePage(driver)
        assert step_one.is_on_page

        # 4. Preencher dados do comprador
        info = users["checkout_info"]
        step_one.fill_buyer_info(
            info["first_name"],
            info["last_name"],
            info["zip_code"],
        )
        step_one.click_continue()

        # 5. Verificar resumo do pedido
        step_two = CheckoutStepTwoPage(driver)
        assert step_two.is_on_page
        assert step_two.item_count == 2

        # 6. Finalizar compra
        step_two.click_finish()

        # 7. Verificar confirmação
        complete = CheckoutCompletePage(driver)
        assert complete.order_confirmed
        assert complete.confirmation_header == CheckoutCompletePage.EXPECTED_HEADER

    def test_confirmation_page_displays_pony_image(self, logged_in, users, driver):
        logged_in.add_to_cart(PRODUCT_1)
        logged_in.header.go_to_cart()
        CartPage(driver).proceed_to_checkout()

        info = users["checkout_info"]
        step_one = CheckoutStepOnePage(driver)
        step_one.fill_buyer_info(info["first_name"], info["last_name"], info["zip_code"])
        step_one.click_continue()
        CheckoutStepTwoPage(driver).click_finish()

        assert CheckoutCompletePage(driver).pony_image_displayed

    def test_back_home_after_purchase_returns_to_inventory(self, logged_in, users, driver):
        logged_in.add_to_cart(PRODUCT_1)
        logged_in.header.go_to_cart()
        CartPage(driver).proceed_to_checkout()

        info = users["checkout_info"]
        step_one = CheckoutStepOnePage(driver)
        step_one.fill_buyer_info(info["first_name"], info["last_name"], info["zip_code"])
        step_one.click_continue()
        CheckoutStepTwoPage(driver).click_finish()

        complete = CheckoutCompletePage(driver)
        complete.go_back_to_products()

        assert "inventory.html" in complete.current_url


@pytest.mark.web
class TestCheckoutStepOneValidation:

    def _go_to_step_one(self, logged_in, driver) -> CheckoutStepOnePage:
        logged_in.add_to_cart(PRODUCT_1)
        logged_in.header.go_to_cart()
        CartPage(driver).proceed_to_checkout()
        return CheckoutStepOnePage(driver)

    def test_missing_first_name_shows_error(self, logged_in, users, driver):
        step_one = self._go_to_step_one(logged_in, driver)
        info = users["checkout_info"]
        step_one.fill_buyer_info("", info["last_name"], info["zip_code"])
        step_one.click_continue()

        assert step_one.has_error
        assert "First Name is required" in step_one.error_message

    def test_missing_last_name_shows_error(self, logged_in, users, driver):
        step_one = self._go_to_step_one(logged_in, driver)
        info = users["checkout_info"]
        step_one.fill_buyer_info(info["first_name"], "", info["zip_code"])
        step_one.click_continue()

        assert step_one.has_error
        assert "Last Name is required" in step_one.error_message

    def test_missing_zip_code_shows_error(self, logged_in, users, driver):
        step_one = self._go_to_step_one(logged_in, driver)
        info = users["checkout_info"]
        step_one.fill_buyer_info(info["first_name"], info["last_name"], "")
        step_one.click_continue()

        assert step_one.has_error
        assert "Postal Code is required" in step_one.error_message

    def test_cancel_checkout_returns_to_cart(self, logged_in, driver):
        step_one = self._go_to_step_one(logged_in, driver)
        step_one.click_cancel()

        assert "cart.html" in step_one.current_url


@pytest.mark.web
class TestCheckoutStepTwoSummary:

    def _go_to_step_two(self, logged_in, users, driver) -> CheckoutStepTwoPage:
        logged_in.add_to_cart(PRODUCT_1)
        logged_in.add_to_cart(PRODUCT_2)
        logged_in.header.go_to_cart()
        CartPage(driver).proceed_to_checkout()
        info = users["checkout_info"]
        step_one = CheckoutStepOnePage(driver)
        step_one.fill_buyer_info(info["first_name"], info["last_name"], info["zip_code"])
        step_one.click_continue()
        return CheckoutStepTwoPage(driver)

    def test_summary_shows_two_items(self, logged_in, users, driver):
        step_two = self._go_to_step_two(logged_in, users, driver)

        assert step_two.item_count == 2

    def test_summary_contains_product_names(self, logged_in, users, driver):
        step_two = self._go_to_step_two(logged_in, users, driver)

        assert PRODUCT_1 in step_two.item_names
        assert PRODUCT_2 in step_two.item_names

    def test_total_equals_subtotal_plus_tax(self, logged_in, users, driver):
        step_two = self._go_to_step_two(logged_in, users, driver)

        assert step_two.total_matches_subtotal_plus_tax

    def test_subtotal_is_positive(self, logged_in, users, driver):
        step_two = self._go_to_step_two(logged_in, users, driver)

        assert step_two.subtotal > 0

    def test_cancel_step_two_returns_to_inventory(self, logged_in, users, driver):
        step_two = self._go_to_step_two(logged_in, users, driver)
        step_two.click_cancel()

        assert "inventory.html" in step_two.current_url
