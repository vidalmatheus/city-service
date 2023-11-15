import json
from datetime import datetime, timedelta

from database.models import City
from fastapi.testclient import TestClient
from pytest_mock.plugin import MockerFixture


def test_fetch_cities(client: TestClient, mocker: MockerFixture):
    mock_cities = [
        {"name": "Rio de Janeiro", "state_abbreviation": "RJ"},
        {"name": "São Paulo", "state_abbreviation": "SP"},
    ]
    mocker.patch("services.city_svc.fetch_cities", return_value=mock_cities)
    resp = client.get("/city/external-fetching")
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert json_resp == mock_cities


def test_fetch_cities_and_save(client: TestClient, mocker: MockerFixture):
    created_qty = 1
    updated_qty = 2
    mock_fetch_and_save_cities = created_qty, updated_qty
    mocker.patch("services.city_svc.fetch_and_save_cities", return_value=mock_fetch_and_save_cities)
    resp = client.post("/city/external-fetching/save")
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert json_resp["message"] == "Fetching and saving completed"
    assert json_resp["created_qty"] == created_qty
    assert json_resp["updated_qty"] == updated_qty


def test_list_cities(client: TestClient, mocker: MockerFixture):
    mock_cities = [
        {
            "id": 1,
            "name": "Rio de Janeiro",
            "state_abbreviation": "RJ",
            "created_at": datetime.utcnow(),
            "updated_at": None,
        },
        {
            "id": 2,
            "name": "São Paulo",
            "state_abbreviation": "SP",
            "created_at": datetime.utcnow() - timedelta(hours=2),
            "updated_at": datetime.utcnow(),
        },
    ]
    mocker.patch("services.city_svc.get_cities", return_value=mock_cities)
    resp = client.get("/city")
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert json_resp[0]["name"] == mock_cities[0]["name"]
    assert json_resp[1]["name"] == mock_cities[1]["name"]


def test_list_cities_params(client: TestClient, mocker: MockerFixture):
    mock_cities = [
        City(
            id=1,
            name="Rio de Janeiro",
            state_abbreviation="RJ",
            created_at=datetime.utcnow(),
        )
    ]
    mocker.patch("services.city_svc.get_cities", return_value=mock_cities)
    resp = client.get("/city", params={"ids": "1,2", "name": "Rio", "state_abbreviation": "RJ"})
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert json_resp[0]["name"] == mock_cities[0].name


def test_get_city_by_id(client: TestClient, mocker: MockerFixture):
    city_id = 1
    mock_city = City(
        id=city_id,
        name="Rio de Janeiro",
        state_abbreviation="RJ",
        created_at=datetime.utcnow(),
    )
    mocker.patch("services.city_svc.get_city_by_id", return_value=mock_city)
    resp = client.get(f"/city/{city_id}")
    assert resp.status_code == 200
    json_resp = json.loads(resp.content)
    assert json_resp["id"] == mock_city.id
    assert json_resp["name"] == mock_city.name
