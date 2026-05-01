import requests


class PetstoreClient:
    """
    Wrapper fino sobre requests.Session que centraliza base_url e
    tratamento de resposta. Cada recurso da API herda desta classe.
    """

    def __init__(self, session: requests.Session):
        self._session = session
        self._base = session.base_url

    def _url(self, path: str) -> str:
        return f"{self._base}{path}"

    def _get(self, path: str, **kwargs) -> requests.Response:
        return self._session.get(self._url(path), **kwargs)

    def _post(self, path: str, **kwargs) -> requests.Response:
        return self._session.post(self._url(path), **kwargs)

    def _put(self, path: str, **kwargs) -> requests.Response:
        return self._session.put(self._url(path), **kwargs)

    def _delete(self, path: str, **kwargs) -> requests.Response:
        return self._session.delete(self._url(path), **kwargs)


class PetClient(PetstoreClient):
    """Operações do recurso /pet."""

    def create(self, payload: dict) -> requests.Response:
        return self._post("/pet", json=payload)

    def get(self, pet_id: int) -> requests.Response:
        return self._get(f"/pet/{pet_id}")

    def update(self, payload: dict) -> requests.Response:
        return self._put("/pet", json=payload)

    def delete(self, pet_id: int) -> requests.Response:
        return self._delete(f"/pet/{pet_id}")

    def find_by_status(self, status: str) -> requests.Response:
        return self._get("/pet/findByStatus", params={"status": status})

    def upload_file(self, pet_id: int, file_path: str) -> requests.Response:
        with open(file_path, "rb") as f:
            return self._session.post(
                self._url(f"/pet/{pet_id}/uploadFile"),
                files={"file": f},
            )


class StoreClient(PetstoreClient):
    """Operações do recurso /store."""

    def inventory(self) -> requests.Response:
        return self._get("/store/inventory")

    def place_order(self, payload: dict) -> requests.Response:
        return self._post("/store/order", json=payload)

    def get_order(self, order_id: int) -> requests.Response:
        return self._get(f"/store/order/{order_id}")

    def delete_order(self, order_id: int) -> requests.Response:
        return self._delete(f"/store/order/{order_id}")


class UserClient(PetstoreClient):
    """Operações do recurso /user."""

    def create(self, payload: dict) -> requests.Response:
        return self._post("/user", json=payload)

    def get(self, username: str) -> requests.Response:
        return self._get(f"/user/{username}")

    def update(self, username: str, payload: dict) -> requests.Response:
        return self._put(f"/user/{username}", json=payload)

    def delete(self, username: str) -> requests.Response:
        return self._delete(f"/user/{username}")

    def login(self, username: str, password: str) -> requests.Response:
        return self._get("/user/login", params={"username": username, "password": password})

    def logout(self) -> requests.Response:
        return self._get("/user/logout")
