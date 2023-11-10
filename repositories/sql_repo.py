from typing import List

from sqlalchemy import insert, select

from database.models import Base
from database.session import Session


class SqlRepository:
    def __init__(self, db: Session, model: Base) -> None:
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

    async def save_bulk(self, data_list: List[dict]) -> List[Base]:
        objs = await self.db.scalars(insert(self.model).returning(self.model), data_list)
        await self.db.commit()
        objs_list = objs.all()
        for obj in objs_list:
            await self.db.refresh(obj)
        return objs_list
