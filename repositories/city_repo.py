from typing import List

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import City
from repositories.sql_repo import SqlRepository


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

        objs = await self.db.execute(select(self.model).where(and_(*filters)))
        return objs.scalars().all()
