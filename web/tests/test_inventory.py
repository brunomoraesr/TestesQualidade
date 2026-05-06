"""
Testes E2E — Inventário do SauceDemo.

Cenários cobertos:
    - Adicionar item ao carrinho atualiza o contador
"""

import pytest


@pytest.mark.web
class TestInventory:

    def test_add_item(self, logged_in):
        logged_in.add_to_cart("Sauce Labs Backpack")

        assert logged_in.cart_item_count == 1
