import pytest

from database.models import City
from repositories.sql_repo import SqlRepository


@pytest.mark.asyncio
async def test_get(db, cities):
    repository = SqlRepository(db, City)
    result = await repository.get()
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_by_id(db, cities):
    repository = SqlRepository(db, City)
    city_id = cities[0].id
    result = await repository.get_by_id(city_id)
    assert result.id == city_id


@pytest.mark.asyncio
async def test_save(db):
    repository = SqlRepository(db, City)
    data = {"name": "Rio de Janeiro", "state_abbreviation": "RJ"}
    result = await repository.save(data)
    assert result.name == "Rio de Janeiro"


@pytest.mark.asyncio
async def test_bulk_create(db):
    repository = SqlRepository(db, City)
    data_list = [
        {"name": "Rio de Janeiro", "state_abbreviation": "RJ"},
        {"name": "São Paulo", "state_abbreviation": "SP"},
    ]
    result = await repository.bulk_create(data_list)
    assert len(result) == 2


@pytest.mark.asyncio
async def test_bulk_update(db, cities):
    repository = SqlRepository(db, City)
    city_id_1 = cities[0].id
    city_id_2 = cities[1].id
    data_list = [{"id": city_id_1, "name": "UpdatedTest1"}, {"id": city_id_2, "name": "UpdatedTest2"}]
    await repository.bulk_update(data_list)
    city_1 = await repository.get_by_id(city_id_1)
    city_2 = await repository.get_by_id(city_id_2)
    assert city_1.name == "UpdatedTest1"
    assert city_2.name == "UpdatedTest2"
