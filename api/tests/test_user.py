"""
Testes de API para o recurso /user do Petstore.

Endpoints cobertos:
    POST   /user               – criar usuário
    GET    /user/{username}    – buscar usuário
    PUT    /user/{username}    – atualizar usuário
    DELETE /user/{username}    – deletar usuário
    GET    /user/login         – autenticar
    GET    /user/logout        – encerrar sessão
"""

import pytest
from api.models.user import User


USERNAME = "john_doe_test"


# ── Helpers ────────────────────────────────────────────────────────────────────

def assert_user_fields(body: dict, expected: dict) -> None:
    """Verifica campos relevantes de um usuário retornado pela API."""
    assert body["username"] == expected["username"]
    assert body["firstName"] == expected["firstName"]
    assert body["lastName"] == expected["lastName"]
    assert body["email"] == expected["email"]
    assert body["phone"] == expected["phone"]


# ── Suite ──────────────────────────────────────────────────────────────────────

@pytest.mark.api
class TestUserCreate:

    def test_create_user_returns_200(self, user_client, user_data):
        payload = user_data["valid_user"]
        response = user_client.create(payload)

        assert response.status_code == 200

    def test_create_user_response_body(self, user_client, user_data):
        payload = user_data["valid_user"]
        response = user_client.create(payload)
        body = response.json()

        assert body["type"] == "unknown"
        assert "message" in body

    def test_create_user_model_serialization(self, user_data):
        """Garante que o dataclass User serializa corretamente para dict."""
        user = User.from_dict(user_data["valid_user"])
        as_dict = user.to_dict()

        assert as_dict["username"] == user_data["valid_user"]["username"]
        assert as_dict["email"] == user_data["valid_user"]["email"]


@pytest.mark.api
class TestUserRead:

    def test_get_existing_user_returns_200(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        response = user_client.get(USERNAME)

        assert response.status_code == 200

    def test_get_existing_user_fields(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        response = user_client.get(USERNAME)
        body = response.json()

        assert_user_fields(body, user_data["valid_user"])

    def test_get_nonexistent_user_returns_404(self, user_client):
        response = user_client.get("usuario_que_nao_existe_xyz_999")

        assert response.status_code == 404

    def test_get_nonexistent_user_error_message(self, user_client):
        response = user_client.get("usuario_que_nao_existe_xyz_999")
        body = response.json()

        assert body["type"] == "error"
        assert "not found" in body["message"].lower()


@pytest.mark.api
class TestUserUpdate:

    def test_update_user_returns_200(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        response = user_client.update(USERNAME, user_data["updated_user"])

        assert response.status_code == 200

    def test_update_user_persists_changes(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        user_client.update(USERNAME, user_data["updated_user"])
        response = user_client.get(USERNAME)
        body = response.json()

        assert body["firstName"] == user_data["updated_user"]["firstName"]
        assert body["lastName"] == user_data["updated_user"]["lastName"]
        assert body["email"] == user_data["updated_user"]["email"]

    def test_update_nonexistent_user_returns_404(self, user_client, user_data):
        response = user_client.update("usuario_inexistente_xyz_999", user_data["updated_user"])

        assert response.status_code == 404


@pytest.mark.api
class TestUserDelete:

    def test_delete_existing_user_returns_200(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        response = user_client.delete(USERNAME)

        assert response.status_code == 200

    def test_delete_removes_user(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        user_client.delete(USERNAME)
        response = user_client.get(USERNAME)

        assert response.status_code == 404

    def test_delete_nonexistent_user_returns_404(self, user_client):
        response = user_client.delete("usuario_inexistente_xyz_999")

        assert response.status_code == 404


@pytest.mark.api
class TestUserLogin:

    def test_login_valid_credentials_returns_200(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        response = user_client.login(USERNAME, user_data["valid_user"]["password"])

        assert response.status_code == 200

    def test_login_returns_session_token(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        response = user_client.login(USERNAME, user_data["valid_user"]["password"])
        body = response.json()

        assert "logged in user session" in body["message"].lower()

    def test_login_sets_rate_limit_headers(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        response = user_client.login(USERNAME, user_data["valid_user"]["password"])

        assert "X-Rate-Limit" in response.headers
        assert "X-Expires-After" in response.headers

    def test_login_invalid_credentials_returns_400(self, user_client):
        response = user_client.login("usuario_invalido", "senha_errada")

        assert response.status_code == 400


@pytest.mark.api
class TestUserLogout:

    def test_logout_returns_200(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        user_client.login(USERNAME, user_data["valid_user"]["password"])
        response = user_client.logout()

        assert response.status_code == 200

    def test_logout_response_message(self, user_client, user_data):
        user_client.create(user_data["valid_user"])
        user_client.login(USERNAME, user_data["valid_user"]["password"])
        response = user_client.logout()
        body = response.json()

        assert body["type"] == "unknown"
        assert "message" in body
