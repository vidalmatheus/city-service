import pytest

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
    mocker.patch(
        "services.city_svc.fetch_cities",
        return_value=[
            {"id": 1, "microrregiao": {"UF": {"sigla": "GO"}}},
        ],
    )
    mock_bulk_create_or_update = mocker.patch.object(CityRepository, "bulk_create_or_update", return_value=[])
    await city_svc.fetch_and_save_cities(db)
    assert city_svc.fetch_cities.called
    assert mock_bulk_create_or_update.called


@pytest.mark.asyncio
async def test_get_cities(mocker, db):
    mock_get = mocker.patch.object(CityRepository, "get", return_value=[])
    params = {
        "ids": [1,2],
        "name": "Rio",
        "state_abbreviation": "RJ"
    }
    await city_svc.get_cities(db, **params)
    assert await mock_get.called_once_with(**params)


@pytest.mark.asyncio
async def test_get_city_by_id(mocker, db):
    mock_get_by_id = mocker.patch.object(CityRepository, "get_by_id", return_value=[])
    city_id = 1
    await city_svc.get_city_by_id(db, city_id)
    assert await mock_get_by_id.called_once_with(city_id)
