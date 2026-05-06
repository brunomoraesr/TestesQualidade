"""
Testes de API — /pet do Petstore.

Cenários cobertos:
    - Criar pet retorna 200 com os dados corretos
    - Buscar pet existente retorna 200
    - Buscar pet inexistente retorna 404
    - Atualizar pet persiste o novo nome
    - Deletar pet remove o recurso
"""

import pytest


PET_ID = 9000001
NONEXISTENT_ID = 999999999


@pytest.mark.api
class TestPet:

    def test_create_returns_200(self, pet_client, pet_data):
        response = pet_client.create(pet_data["valid_pet"])

        assert response.status_code == 200
        assert response.json()["id"] == PET_ID

    def test_get_existing_returns_200(self, pet_client, pet_data):
        pet_client.create(pet_data["valid_pet"])
        response = pet_client.get(PET_ID)

        assert response.status_code == 200
        assert response.json()["name"] == pet_data["valid_pet"]["name"]

    @pytest.mark.xfail(
        reason="O Petstore público é compartilhado — o ID pode ter sido criado por outro cliente "
               "e o recurso deixar de ser inexistente entre execuções.",
        strict=False,
    )
    def test_get_nonexistent_returns_404(self, pet_client):
        response = pet_client.get(NONEXISTENT_ID)

        assert response.status_code == 404

    def test_update_persists_name(self, pet_client, pet_data):
        pet_client.create(pet_data["valid_pet"])
        pet_client.update(pet_data["updated_pet"])
        response = pet_client.get(PET_ID)

        assert response.json()["name"] == pet_data["updated_pet"]["name"]

    def test_delete_removes_pet(self, pet_client, pet_data):
        pet_client.create(pet_data["valid_pet"])
        pet_client.delete(PET_ID)
        response = pet_client.get(PET_ID)

        assert response.status_code == 404
