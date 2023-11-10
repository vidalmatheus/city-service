from sqlalchemy.ext.asyncio import AsyncSession

from adapters.ibge.ibge_api import IbgeAPI
from database.models import City
from repositories.sql_repo import SqlRepository


def fetch_cities():
    cities_list = IbgeAPI().fetch_cities()
    return cities_list


async def fetch_and_save_cities(db: AsyncSession):
    cities_list = fetch_cities()
    city_repo = SqlRepository(db, City)
    cities_list_db = await city_repo.save_bulk(cities_list)
    return cities_list_db


async def get_cities(db: AsyncSession):
    cities_list = await SqlRepository(db, City).get()
    return cities_list


async def get_city_by_id(db: AsyncSession, id: int):
    city = await SqlRepository(db, City).get_by_id(id)
    return city
