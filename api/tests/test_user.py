"""
Testes de API — /user do Petstore.

Cenários cobertos:
    - Criar usuário retorna 200
    - Buscar usuário existente retorna 200
    - Buscar usuário inexistente retorna 404
    - Login retorna 200 com token de sessão
"""

import pytest


USERNAME = "john_doe_test"


@pytest.mark.api
class TestUser:

    def test_create_returns_200(self, user_client, user_data):
        response = user_client.create(user_data["valid_user"])

        assert response.status_code == 200

    def test_get_existing_returns_200(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        response = user_client.get(USERNAME)

        assert response.status_code == 200

    def test_get_nonexistent_returns_404(self, user_client):
        response = user_client.get("usuario_que_nao_existe_xyz_999")

        assert response.status_code == 404

    def test_login_returns_200(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        response = user_client.login(USERNAME, user_data["valid_user"]["password"])

        assert response.status_code == 200
        assert "logged in user session" in response.json()["message"].lower()
