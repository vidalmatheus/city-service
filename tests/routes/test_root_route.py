from fastapi.testclient import TestClient


def test_fetch_cities(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.history[0].status_code == 307
