import json
from pathlib import Path

import pytest

from api.clients.petstore_client import PetClient, StoreClient, UserClient


FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def pet_client(api_session):
    return PetClient(api_session)


@pytest.fixture(scope="session")
def store_client(api_session):
    return StoreClient(api_session)


@pytest.fixture(scope="session")
def user_client(api_session):
    return UserClient(api_session)


@pytest.fixture(scope="session")
def pet_data():
    with open(FIXTURES_DIR / "pet_data.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def order_data():
    with open(FIXTURES_DIR / "order_data.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def user_data():
    with open(FIXTURES_DIR / "user_data.json", encoding="utf-8") as f:
        return json.load(f)
