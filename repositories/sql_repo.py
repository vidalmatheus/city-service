from typing import List

from sqlalchemy import and_, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import Base

MAX_RECORDS = 100


class SqlRepository:
    def __init__(self, db: AsyncSession, model: Base, log_model: Base = None) -> None:
        self.db = db
        self.model = model
        self.log_model = log_model

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

    async def get_log(self, params: dict = None, limit: int = MAX_RECORDS) -> List[Base]:
        conditions = []
        if params is not None:
            for key, value in params.items():
                column = getattr(self.log_model, key, None)
                if value:
                    if key == "ids":
                        column = getattr(self.log_model, "id", None)
                        conditions.append(column.in_(value))
                    elif key == "status":
                        conditions.append(column.icontains(value))
                    else:
                        conditions.append(column == value)

        query = (
            select(self.log_model)
            .options(joinedload(self.log_model.city))
            .where(and_(*conditions))
            .order_by(self.log_model.created_at.desc())
            .limit(limit)
        )

        objs = await self.db.execute(query)
        return objs.scalars().all()

    async def get_most_recent_logs_by_status(self, status: str = None, limit: int = MAX_RECORDS):
        column_foreign_key = f"{self.model.__tablename__}_id"
        group_by_column = getattr(self.log_model, column_foreign_key, None)
        query = (
            select(self.log_model, func.max(self.log_model.created_at).label("max_created_at"))
            .group_by(group_by_column)
            .options(joinedload(self.log_model.city))
            .where(self.log_model.status.icontains(status))
            .order_by(func.max(self.log_model.created_at).desc())
            .limit(limit)
        )

        objs = await self.db.execute(query)
        return objs.scalars().all()

    async def save_log(self, params: dict) -> Base:
        obj = self.log_model(**params)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj, attribute_names=[self.model.__tablename__])
        return obj
