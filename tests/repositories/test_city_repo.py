import pytest

from repositories.city_repo import CityRepository


@pytest.mark.asyncio
async def test_get(db, cities):
    repository = CityRepository(db)
    result = await repository.get()
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_params(db, cities):
    repository = CityRepository(db)
    result = await repository.get(ids=[cities[0].id], name="Rio", state_abbreviation="RJ")
    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_by_name(db):
    repository = CityRepository(db)
    await repository.bulk_create(
        [{"name": "Monsenhor Paulo", "state_abbreviation": "MG"}, {"name": "São Paulo", "state_abbreviation": "SP"}]
    )
    result_1 = await repository.get(name="sao")
    result_2 = await repository.get(name="paulo")
    assert len(result_1) == 1
    assert len(result_2) == 2


@pytest.mark.asyncio
async def test_get_by_id(db, cities):
    repository = CityRepository(db)
    city_id = 1
    result = await repository.get_by_id(city_id)
    assert result.id == city_id


@pytest.mark.asyncio
async def test_save(db):
    repository = CityRepository(db)
    data = {"name": "São Paulo", "normalized_name": "Sao Paulo", "state_abbreviation": "SP"}
    result = await repository.save(data)
    assert result.name == "São Paulo"
    assert result.normalized_name == "Sao Paulo"
    assert str(result)


@pytest.mark.asyncio
async def test_bulk_create_or_update(db, cities):
    repository = CityRepository(db)
    created_qty, updated_qty = await repository.bulk_create_or_update(
        [{"name": "Rio de Janeiro", "state_abbreviation": "RJ"}, {"name": "Salvador", "state_abbreviation": "BA"}]
    )
    assert created_qty == 1
    assert updated_qty == 1
