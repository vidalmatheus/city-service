import pytest

from database.models import City, CityLog, CityLogStatus
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
    data = {"name": "São Paulo", "normalized_name": "Sao Paulo", "state_abbreviation": "SP"}
    result = await repository.save(data)
    assert result.name == "São Paulo"
    assert result.normalized_name == "Sao Paulo"
    assert str(result)


@pytest.mark.asyncio
async def test_save_invalid_state_abbreviation(db):
    repository = SqlRepository(db, City)
    data = {"name": "Rio de Janeiro", "normalized_name": "Rio de Janeiro", "state_abbreviation": "R"}
    with pytest.raises(ValueError, match="State abbreviation must be a two-letter uppercase string"):
        await repository.save(data)


@pytest.mark.asyncio
async def test_bulk_create(db):
    repository = SqlRepository(db, City)
    data_list = [
        {"name": "Rio de Janeiro", "normalized_name": "Rio de Janeiro", "state_abbreviation": "RJ"},
        {"name": "São Paulo", "normalized_name": "Sao Paulo", "state_abbreviation": "SP"},
    ]
    result = await repository.bulk_create(data_list)
    assert len(result) == 2


@pytest.mark.asyncio
async def test_bulk_create_no_data(db):
    repository = SqlRepository(db, City)
    data_list = []
    result = await repository.bulk_create(data_list)
    assert len(result) == 0


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


@pytest.mark.asyncio
async def test_bulk_update_no_data(db):
    repository = SqlRepository(db, City)
    data_list = []
    result = await repository.bulk_update(data_list)
    assert len(result) == 0


@pytest.mark.asyncio
async def test_get_log(db, cities_log):
    repo = SqlRepository(db, City, CityLog)
    result = await repo.get_log({"ids": [1, 2, 3], "city_id": 1, "status": CityLogStatus.CREATED})
    assert len(result) == 1
    assert result[0].status == CityLogStatus.CREATED
    result_2 = await repo.get_log({"ids": None, "city_id": None, "status": None})
    assert len(result_2) == 4
    result_3 = await repo.get_log()
    assert len(result_3) == 4


@pytest.mark.asyncio
async def test_get_most_recent_logs_by_status(db, cities_log):
    repo = SqlRepository(db, City, CityLog)
    result = await repo.get_most_recent_logs_by_status(CityLogStatus.CREATED)
    assert len(result) == 2
    result_2 = await repo.get_most_recent_logs_by_status(CityLogStatus.SELECTED)
    assert len(result_2) == 2


@pytest.mark.asyncio
async def test_save_log(db, cities):
    repo = SqlRepository(db, City, CityLog)
    city = cities[0]
    city_id = city.id
    status = CityLogStatus.SELECTED
    result: CityLog = await repo.save_log({"city_id": city_id, "status": status})
    assert result.city == city
    assert result.city_id == city_id
    assert result.status == CityLogStatus.SELECTED
    assert str(result)
