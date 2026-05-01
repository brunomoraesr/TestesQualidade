import json
from pathlib import Path

import pytest

from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage
from web.pages.checkout_page import (
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


# ── Dados de teste ─────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def users():
    with open(FIXTURES_DIR / "users.json", encoding="utf-8") as f:
        return json.load(f)


# ── Page Objects ───────────────────────────────────────────────────────────────

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def inventory_page(driver):
    return InventoryPage(driver)


@pytest.fixture
def cart_page(driver):
    return CartPage(driver)


@pytest.fixture
def checkout_step_one(driver):
    return CheckoutStepOnePage(driver)


@pytest.fixture
def checkout_step_two(driver):
    return CheckoutStepTwoPage(driver)


@pytest.fixture
def checkout_complete(driver):
    return CheckoutCompletePage(driver)


# ── Fixtures compostas (estado pré-configurado) ────────────────────────────────

@pytest.fixture
def logged_in(driver, users):
    """Abre o browser já autenticado como standard_user.
    Aguarda a lista de produtos ficar visível antes de retornar,
    garantindo que a página carregou completamente."""
    page = LoginPage(driver)
    page.open()
    page.login(users["standard"]["username"], users["standard"]["password"])
    page._wait_for_url_contains("inventory.html")
    inventory = InventoryPage(driver)
    inventory.wait_for_page_load()  # aguarda lista de produtos E sort dropdown
    return inventory


@pytest.fixture
def cart_with_one_item(logged_in, users):
    """Usuário logado com um item no carrinho (Sauce Labs Backpack)."""
    logged_in.add_to_cart("Sauce Labs Backpack")
    return CartPage(logged_in._driver)
