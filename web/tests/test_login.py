"""
Testes E2E — Login do SauceDemo.

Cenários cobertos:
    - Login com sucesso redireciona para inventário
    - Login com credenciais inválidas exibe mensagem de erro
    - Login com usuário bloqueado exibe mensagem específica
    - Campos vazios disparam validação
    - Botão X fecha a mensagem de erro
"""

import pytest

from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage


@pytest.mark.web
class TestLoginSuccess:

    def test_login_redirects_to_inventory(self, login_page, users):
        login_page.open()
        login_page.login(
            users["standard"]["username"],
            users["standard"]["password"],
        )

        assert "inventory.html" in login_page.current_url

    def test_login_shows_product_list(self, login_page, users, driver):
        login_page.open()
        login_page.login(
            users["standard"]["username"],
            users["standard"]["password"],
        )
        inventory = InventoryPage(driver)

        assert inventory.is_on_page

    def test_login_with_fluent_api(self, login_page, users):
        login_page.open()
        login_page.enter_username(users["standard"]["username"])
        login_page.enter_password(users["standard"]["password"])
        login_page.click_login()

        assert "inventory.html" in login_page.current_url


@pytest.mark.web
class TestLoginFailure:

    def test_invalid_credentials_show_error(self, login_page, users):
        login_page.open()
        login_page.login(
            users["invalid"]["username"],
            users["invalid"]["password"],
        )

        assert login_page.has_error

    def test_invalid_credentials_error_message_content(self, login_page, users):
        login_page.open()
        login_page.login(
            users["invalid"]["username"],
            users["invalid"]["password"],
        )

        assert "Username and password do not match" in login_page.error_message

    def test_locked_user_shows_specific_error(self, login_page, users):
        login_page.open()
        login_page.login(
            users["locked_out"]["username"],
            users["locked_out"]["password"],
        )

        assert "locked out" in login_page.error_message.lower()

    def test_empty_username_shows_error(self, login_page, users):
        login_page.open()
        login_page.login("", users["standard"]["password"])

        assert "Username is required" in login_page.error_message

    def test_empty_password_shows_error(self, login_page, users):
        login_page.open()
        login_page.login(users["standard"]["username"], "")

        assert "Password is required" in login_page.error_message

    def test_error_button_dismisses_message(self, login_page, users):
        login_page.open()
        login_page.login(
            users["invalid"]["username"],
            users["invalid"]["password"],
        )
        assert login_page.has_error

        login_page.dismiss_error()

        assert not login_page.has_error

    def test_url_stays_on_login_after_failure(self, login_page, users):
        login_page.open()
        login_page.login(
            users["invalid"]["username"],
            users["invalid"]["password"],
        )

        assert "inventory.html" not in login_page.current_url
