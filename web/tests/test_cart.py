"""
Testes E2E — Carrinho de compras do SauceDemo.

Cenários cobertos:
    - Item adicionado aparece no carrinho
    - Preço no carrinho corresponde ao do inventário
    - Quantidade de itens está correta
    - Remover item do carrinho
    - Botão "Continue Shopping" retorna ao inventário
"""

import pytest

from web.pages.cart_page import CartPage


@pytest.mark.web
class TestCartContents:

    def test_added_item_appears_in_cart(self, logged_in, driver):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.header.go_to_cart()
        cart = CartPage(driver)

        assert cart.contains_item("Sauce Labs Backpack")

    def test_cart_shows_correct_item_count(self, logged_in, driver):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.add_to_cart("Sauce Labs Bike Light")
        logged_in.header.go_to_cart()
        cart = CartPage(driver)

        assert cart.item_count == 2

    def test_cart_item_price_matches_inventory(self, logged_in, driver):
        backpack_price = logged_in.product_prices[
            logged_in.product_names.index("Sauce Labs Backpack")
        ]
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.header.go_to_cart()
        cart = CartPage(driver)

        assert cart.item_prices[0] == backpack_price

    def test_cart_item_quantity_is_one(self, logged_in, driver):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.header.go_to_cart()
        cart = CartPage(driver)

        assert cart.item_quantities[0] == 1

    def test_two_different_items_in_cart(self, logged_in, driver):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.add_to_cart("Sauce Labs Bike Light")
        logged_in.header.go_to_cart()
        cart = CartPage(driver)

        assert cart.contains_item("Sauce Labs Backpack")
        assert cart.contains_item("Sauce Labs Bike Light")


@pytest.mark.web
class TestCartActions:

    def test_remove_item_empties_cart(self, logged_in, driver):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.header.go_to_cart()
        cart = CartPage(driver)
        cart.remove_item("Sauce Labs Backpack")

        assert cart.is_empty

    def test_remove_one_of_two_items(self, logged_in, driver):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.add_to_cart("Sauce Labs Bike Light")
        logged_in.header.go_to_cart()
        cart = CartPage(driver)
        cart.remove_item("Sauce Labs Backpack")

        assert cart.item_count == 1
        assert cart.contains_item("Sauce Labs Bike Light")
        assert not cart.contains_item("Sauce Labs Backpack")

    def test_continue_shopping_returns_to_inventory(self, logged_in, driver):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.header.go_to_cart()
        cart = CartPage(driver)
        cart.continue_shopping()

        assert "inventory.html" in cart.current_url
