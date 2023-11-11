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
async def test_bulk_create_or_update(db, cities):
    repository = CityRepository(db)
    created_qtd, updated_qtd = await repository.bulk_create_or_update([
        {
            "name": "Rio de Janeiro",
            "state_abbreviation": "RJ"
		},
        {
            "name": "Salvador",
            "state_abbreviation": "BA"
		}
	])
    assert created_qtd == 1
    assert updated_qtd == 1
