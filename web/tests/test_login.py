"""
Testes E2E — Login do SauceDemo.

Cenários cobertos:
    - Login com sucesso redireciona para inventário
    - Login com credenciais inválidas exibe mensagem de erro
"""

import pytest


@pytest.mark.web
class TestLogin:

    def test_success(self, login_page, users):
        login_page.open()
        login_page.login(users["standard"]["username"], users["standard"]["password"])

        assert "inventory.html" in login_page.current_url

    def test_invalid_credentials(self, login_page, users):
        login_page.open()
        login_page.login(users["invalid"]["username"], users["invalid"]["password"])

        assert "Username and password do not match" in login_page.error_message
