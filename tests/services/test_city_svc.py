import pytest

from database.models import City, CityLog, CityLogStatus
from repositories.city_repo import CityRepository
from services import city_svc


def test_fetch_cities(mocker):
    mock_cities = [
        {"id": 1, "microrregiao": {"UF": {"sigla": "GO"}}},
    ]
    mocker.patch("adapters.ibge.ibge_api.IbgeAPI.fetch_cities", return_value=mock_cities)
    res = city_svc.fetch_cities()
    assert res == mock_cities


@pytest.mark.asyncio
async def test_fetch_and_save_cities(mocker, db):
    cities_list = [
        {"id": 1, "microrregiao": {"UF": {"sigla": "GO"}}},
    ]
    mocker.patch(
        "services.city_svc.fetch_cities",
        return_value=cities_list,
    )
    mock_bulk_create_or_update = mocker.patch.object(CityRepository, "bulk_create_or_update", return_value=(1, 0))
    result = await city_svc.fetch_and_save_cities(db)
    assert result == (1, 0)
    assert city_svc.fetch_cities.called
    mock_bulk_create_or_update.assert_awaited_once_with(cities_list)


@pytest.mark.asyncio
async def test_get_cities(mocker, db):
    mock_get = mocker.patch.object(CityRepository, "get", return_value=[])
    params = {"ids": [1, 2], "name": "Rio", "state_abbreviation": "RJ"}
    result = await city_svc.get_cities(db, **params)
    assert result == []
    mock_get.assert_awaited_once_with(*params.values())


@pytest.mark.asyncio
async def test_get_city_by_id(mocker, db):
    mock_get_by_id = mocker.patch.object(CityRepository, "get_by_id", return_value={})
    city_id = 1
    result = await city_svc.get_city_by_id(db, city_id)
    assert result == {}
    mock_get_by_id.assert_awaited_once_with(city_id)


@pytest.mark.asyncio
async def test_create_city_log(mocker, db):
    mock_create_city_log = mocker.patch.object(CityRepository, "save_log", return_value={})
    city_id = 1
    status = CityLogStatus.SELECTED
    result = await city_svc.create_city_log(db, city_id, status)
    assert result == {}
    mock_create_city_log.assert_awaited_once_with({"city_id": city_id, "status": status})


@pytest.mark.asyncio
async def test_get_city_log(mocker, db):
    mock_get_city_log = mocker.patch.object(CityRepository, "get_log", return_value=[])
    ids = [1]
    city_id = 1
    status = CityLogStatus.SELECTED
    result = await city_svc.get_city_log(db, ids, city_id, status)
    assert result == []
    mock_get_city_log.assert_awaited_once_with({"ids": ids, "city_id": city_id, "status": status})


@pytest.mark.asyncio
async def test_get_most_recent_selected_cities(mocker, db):
    city = City()
    city_log = CityLog(city=city, status=CityLogStatus.SELECTED)
    mock_get_most_recent_selected_cities = mocker.patch.object(
        CityRepository, "get_most_recent_logs_by_status", return_value=[city_log]
    )
    status = CityLogStatus.SELECTED
    result = await city_svc.get_most_recent_selected_cities(db, status)
    assert result == [city]
    mock_get_most_recent_selected_cities.assert_awaited_once_with(status)
