from datetime import datetime
from typing import List

from sqlalchemy import and_, select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import City, CityLog
from repositories.sql_repo import SqlRepository
from utils import str_utils

MAX_RECORDS = 100


class CityRepository(SqlRepository):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, City, CityLog)

    def _add_normalized_name(self, city: dict = None, cities: List[dict] = None):
        if city:
            city["normalized_name"] = str_utils.only_ascii(city["name"])
            return city
        for city in cities:
            city["normalized_name"] = str_utils.only_ascii(city["name"])
        return cities

    async def get(self, ids: List[int] = None, name: str = None, state_abbreviation: str = None) -> List[City]:
        filters = []

        if ids:
            filters.append(City.id.in_(ids))

        if name:
            filters.append(City.normalized_name.icontains(str_utils.only_ascii(name)))

        if state_abbreviation:
            filters.append(City.state_abbreviation.istartswith(state_abbreviation))

        objs = await self.db.execute(
            select(City).where(and_(True, *filters)).limit(MAX_RECORDS).order_by(City.normalized_name)
        )
        return objs.scalars().all()

    async def get_by_id(self, id: int) -> City:
        return await super().get_by_id(id)

    async def save(self, city: dict) -> City:
        self._add_normalized_name(city)
        return await super().save(city)

    async def bulk_create(self, cities: List[dict]) -> List[City]:
        self._add_normalized_name(cities=cities)
        return await super().bulk_create(cities)

    async def bulk_update(self, data_list: List[dict]) -> List[City]:
        return await super().bulk_update(data_list)

    async def bulk_create_or_update(self, cities: List[dict]) -> List[City]:
        to_be_updated_objects = []
        to_be_created_objects = []
        now = datetime.utcnow()
        existing_cities = await self.db.execute(
            select(City).filter(
                tuple_(City.name, City.state_abbreviation).in_(
                    ((city["name"], city["state_abbreviation"]) for city in cities)
                )
            )
        )
        existing_cities = existing_cities.scalars().all()
        existing_cities_map = {(city.name, city.state_abbreviation): city for city in existing_cities}

        for city in cities:
            existing_city = existing_cities_map.get((city["name"], city["state_abbreviation"]))
            if existing_city:
                existing_city_dict = existing_city.to_dict(only=("id", "name", "state_abbreviation", "updated_at"))
                existing_city_dict["updated_at"] = now
                to_be_updated_objects.append(existing_city_dict)
            else:
                to_be_created_objects.append(city)

        created_objs = await self.bulk_create(to_be_created_objects)
        updated_objs = await self.bulk_update(to_be_updated_objects)
        return len(created_objs), len(updated_objs)
