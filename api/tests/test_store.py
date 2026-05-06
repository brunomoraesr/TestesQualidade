"""
Testes de API — /store do Petstore.

Cenários cobertos:
    - Criar pedido retorna 200 com os dados corretos
    - Buscar pedido existente retorna 200
    - Buscar pedido inexistente retorna 404
    - Deletar pedido remove o recurso
"""

import pytest


ORDER_ID = 5
NONEXISTENT_ORDER_ID = 999999


@pytest.mark.api
class TestStore:

    def test_place_order_returns_200(self, store_client, order_data):
        response = store_client.place_order(order_data["valid_order"])

        assert response.status_code == 200
        assert response.json()["status"] == "placed"

    def test_get_order_returns_200(self, store_client, order_data):
        store_client.place_order(order_data["valid_order"])
        response = store_client.get_order(ORDER_ID)

        assert response.status_code == 200

    def test_get_nonexistent_order_returns_404(self, store_client):
        response = store_client.get_order(NONEXISTENT_ORDER_ID)

        assert response.status_code == 404

    def test_delete_order_removes_it(self, store_client, order_data):
        store_client.place_order(order_data["valid_order"])
        store_client.delete_order(ORDER_ID)
        response = store_client.get_order(ORDER_ID)

        assert response.status_code == 404
