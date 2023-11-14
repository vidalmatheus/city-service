from typing import List

from sqlalchemy import event
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Base


class SqlRepository:
    def __init__(self, db: AsyncSession, model: Base) -> None:
        self.db = db
        self.model = model

    async def get(self) -> List[Base]:
        objs = await self.db.execute(select(self.model))
        return objs.scalars().all()

    async def get_by_id(self, id: int) -> Base:
        objs = await self.db.execute(select(self.model).where(self.model.id == id))
        return objs.scalar()

    async def save(self, data: dict) -> Base:
        obj = self.model(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def bulk_create(self, data_list: List[dict]) -> List[Base]:
        if not data_list:
            return []
        objs = await self.db.execute(insert(self.model).values(data_list).returning(self.model))
        await self.db.commit()
        return objs.scalars().all()

    async def bulk_update(self, data_list: List[dict]) -> List[Base]:
        if not data_list:
            return []
        # Dialect sqlite+aiosqlite with current server capabilities does not support UPDATE..RETURNING when executemany is used
        await self.db.execute(update(self.model), data_list)
        await self.db.commit()
        return data_list
