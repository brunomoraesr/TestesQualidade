"""
Testes E2E — Inventário e contador do carrinho do SauceDemo.

Cenários cobertos:
    - Página de inventário carrega 6 produtos
    - Contador do carrinho atualiza ao adicionar 1 item
    - Contador do carrinho atualiza ao adicionar 2 itens
    - Contador some ao remover o único item
    - Ordenação de produtos funciona (A→Z, Z→A, preço)
"""

import pytest


@pytest.mark.web
class TestInventoryPage:

    def test_inventory_loads_six_products(self, logged_in):
        assert logged_in.product_count == 6

    def test_inventory_is_on_page(self, logged_in):
        assert logged_in.is_on_page

    def test_product_names_are_not_empty(self, logged_in):
        names = logged_in.product_names
        assert len(names) == 6
        assert all(name for name in names)

    def test_product_prices_are_positive(self, logged_in):
        prices = logged_in.product_prices
        assert all(price > 0 for price in prices)


@pytest.mark.web
class TestCartCounter:

    def test_badge_absent_before_adding_items(self, logged_in):
        assert not logged_in.header.cart_badge_is_visible

    def test_counter_shows_one_after_adding_one_item(self, logged_in):
        logged_in.add_to_cart("Sauce Labs Backpack")

        assert logged_in.cart_item_count == 1

    def test_counter_shows_two_after_adding_two_items(self, logged_in):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.add_to_cart("Sauce Labs Bike Light")

        assert logged_in.cart_item_count == 2

    def test_counter_decrements_after_removing_item(self, logged_in):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.add_to_cart("Sauce Labs Bike Light")
        logged_in.remove_from_cart("Sauce Labs Backpack")

        assert logged_in.cart_item_count == 1

    def test_badge_disappears_after_removing_only_item(self, logged_in):
        logged_in.add_to_cart("Sauce Labs Backpack")
        logged_in.remove_from_cart("Sauce Labs Backpack")

        assert not logged_in.header.cart_badge_is_visible

    def test_counter_reflects_all_six_items_added(self, logged_in):
        logged_in.add_all_to_cart()

        assert logged_in.cart_item_count == 6


@pytest.mark.web
class TestProductSorting:

    def test_sort_az_orders_alphabetically(self, logged_in):
        logged_in.sort_by("az")
        names = logged_in.product_names

        assert names == sorted(names)

    def test_sort_za_orders_reverse_alphabetically(self, logged_in):
        logged_in.sort_by("za")
        names = logged_in.product_names

        assert names == sorted(names, reverse=True)

    def test_sort_lohi_orders_by_price_ascending(self, logged_in):
        logged_in.sort_by("lohi")
        prices = logged_in.product_prices

        assert prices == sorted(prices)

    def test_sort_hilo_orders_by_price_descending(self, logged_in):
        logged_in.sort_by("hilo")
        prices = logged_in.product_prices

        assert prices == sorted(prices, reverse=True)
