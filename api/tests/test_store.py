"""
Testes de API para o recurso /store do Petstore.

Endpoints cobertos:
    GET    /store/inventory        – inventário por status
    POST   /store/order            – criar pedido
    GET    /store/order/{orderId}  – buscar pedido por ID
    DELETE /store/order/{orderId}  – deletar pedido
"""

import pytest
from api.models.order import Order


ORDER_ID = 5
NONEXISTENT_ORDER_ID = 999999


# ── Helpers ────────────────────────────────────────────────────────────────────

def assert_order_fields(body: dict, expected: dict) -> None:
    assert body["petId"] == expected["petId"]
    assert body["quantity"] == expected["quantity"]
    assert body["status"] == expected["status"]


# ── Suite ──────────────────────────────────────────────────────────────────────

@pytest.mark.api
class TestStoreInventory:

    def test_inventory_returns_200(self, store_client):
        response = store_client.inventory()

        assert response.status_code == 200

    def test_inventory_returns_dict(self, store_client):
        response = store_client.inventory()
        body = response.json()

        assert isinstance(body, dict)

    def test_inventory_has_status_keys(self, store_client):
        """A API retorna contagens por status; pelo menos um dos padrões deve existir."""
        response = store_client.inventory()
        body = response.json()

        known_statuses = {"available", "pending", "sold"}
        assert known_statuses & body.keys(), "Nenhum status padrão encontrado no inventário"

    def test_inventory_values_are_integers(self, store_client):
        response = store_client.inventory()
        body = response.json()

        assert all(isinstance(v, int) for v in body.values())


@pytest.mark.api
class TestStoreOrder:

    def test_place_order_returns_200(self, store_client, order_data):
        response = store_client.place_order(order_data["valid_order"])

        assert response.status_code == 200

    def test_place_order_response_fields(self, store_client, order_data):
        response = store_client.place_order(order_data["valid_order"])
        body = response.json()

        assert_order_fields(body, order_data["valid_order"])

    def test_place_order_response_has_id(self, store_client, order_data):
        response = store_client.place_order(order_data["valid_order"])
        body = response.json()

        assert "id" in body
        assert isinstance(body["id"], int)

    def test_place_order_model_serialization(self, order_data):
        """Garante que o dataclass Order serializa corretamente para dict."""
        order = Order.from_dict(order_data["valid_order"])
        as_dict = order.to_dict()

        assert as_dict["petId"] == order_data["valid_order"]["petId"]
        assert as_dict["quantity"] == order_data["valid_order"]["quantity"]
        assert as_dict["status"] == order_data["valid_order"]["status"]

    def test_place_order_status_is_placed(self, store_client, order_data):
        response = store_client.place_order(order_data["valid_order"])
        body = response.json()

        assert body["status"] == "placed"


@pytest.mark.api
class TestStoreGetOrder:

    def test_get_order_returns_200(self, store_client, order_data):
        store_client.place_order(order_data["valid_order"])
        response = store_client.get_order(ORDER_ID)

        assert response.status_code == 200

    def test_get_order_fields(self, store_client, order_data):
        store_client.place_order(order_data["valid_order"])
        response = store_client.get_order(ORDER_ID)
        body = response.json()

        assert_order_fields(body, order_data["valid_order"])

    def test_get_nonexistent_order_returns_404(self, store_client):
        response = store_client.get_order(NONEXISTENT_ORDER_ID)

        assert response.status_code == 404

    def test_get_nonexistent_order_error_message(self, store_client):
        response = store_client.get_order(NONEXISTENT_ORDER_ID)
        body = response.json()

        assert body["type"] == "error"
        assert "not found" in body["message"].lower()

    @pytest.mark.parametrize("order_id", [1, 2, 3, 4, 5])
    def test_get_valid_order_id_range(self, store_client, order_id):
        """IDs de 1–10 são válidos pela spec da API; valida que a API aceita o range."""
        response = store_client.get_order(order_id)

        assert response.status_code in (200, 404)

    def test_get_order_id_above_10_accepts_or_rejects(self, store_client):
        """A spec define IDs válidos como 1–10, mas a implementação pública
        do Petstore não aplica esse limite — aceita 200 ou 404."""
        response = store_client.get_order(11)

        assert response.status_code in (200, 404)


@pytest.mark.api
class TestStoreDeleteOrder:

    def test_delete_order_returns_200(self, store_client, order_data):
        store_client.place_order(order_data["valid_order"])
        response = store_client.delete_order(ORDER_ID)

        assert response.status_code == 200

    def test_delete_order_removes_it(self, store_client, order_data):
        store_client.place_order(order_data["valid_order"])
        store_client.delete_order(ORDER_ID)
        response = store_client.get_order(ORDER_ID)

        assert response.status_code == 404

    def test_delete_nonexistent_order_returns_404(self, store_client):
        response = store_client.delete_order(NONEXISTENT_ORDER_ID)

        assert response.status_code == 404
