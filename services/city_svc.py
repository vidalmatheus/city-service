from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from adapters.ibge.ibge_api import IbgeAPI
from database.models import CityLogStatus
from repositories.city_repo import CityRepository


def fetch_cities():
    cities_list = IbgeAPI().fetch_cities()
    return cities_list


async def fetch_and_save_cities(db: AsyncSession):
    cities_list = fetch_cities()
    city_repo = CityRepository(db)
    return await city_repo.bulk_create_or_update(cities_list)


async def get_cities(db: AsyncSession, ids: List[int] = None, name: str = None, state_abbreviation: str = None):
    cities_list = await CityRepository(db).get(ids, name, state_abbreviation)
    return cities_list


async def get_city_by_id(db: AsyncSession, id: int):
    city = await CityRepository(db).get_by_id(id)
    return city


async def create_city_log(db: AsyncSession, city_id: int, status: str):
    repo = CityRepository(db)
    log = await repo.save_log({"city_id": city_id, "status": status})
    return log


async def get_city_log(db: AsyncSession, ids: List[int] = None, city_id: int = None, status: str = None):
    repo = CityRepository(db)
    logs = await repo.get_log({"ids": ids, "city_id": city_id, "status": status})
    return logs


async def get_most_recent_selected_cities(db: AsyncSession, status: CityLogStatus):
    repo = CityRepository(db)
    last_10_logs = await repo.get_most_recent_logs_by_status(status=status, limit=10)
    most_recent_selected_cities = [log.city for log in last_10_logs]
    return most_recent_selected_cities
