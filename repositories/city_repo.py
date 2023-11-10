from typing import List
from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import City
from repositories.sql_repo import SqlRepository

MAX_RECORDS = 100


class CityRepository(SqlRepository):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, City)

    async def get(self, ids: List[int] = None, name: str = None, state_abbreviation: str = None) -> List[City]:
        filters = []

        if ids:
            filters.append(City.id.in_(ids))

        if name:
            filters.append(City.name.istartswith(name))

        if state_abbreviation:
            filters.append(City.state_abbreviation.istartswith(state_abbreviation))

        objs = await self.db.execute(select(City).where(and_(*filters)).limit(MAX_RECORDS))
        return objs.scalars().all()

    async def bulk_create_or_update(self, cities: List[dict]) -> List[City]:
        to_be_updated_objects = []
        to_be_created_objects = []
        for city in cities:
            existing_city_query_result = await self.db.execute(select(City).where(
                and_(
                    City.name == city["name"],
                    City.state_abbreviation == city["state_abbreviation"]
                )
            ))
            existing_city = existing_city_query_result.scalar()
            if existing_city:
                existing_city_dict = existing_city.to_dict()
                existing_city_dict.pop("created")
                existing_city_dict["updated"] = datetime.utcnow()
                to_be_updated_objects.append(existing_city_dict)
            else:
                to_be_created_objects.append(city)

        created_objs = await self.bulk_create(to_be_created_objects)
        updated_objs = await self.bulk_update(to_be_updated_objects)
        return len(created_objs), len(updated_objs)

        
