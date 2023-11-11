from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db_session
from schemas.response_schemas import FetchCitySchema, FetchSaveCitySchema, GetCitySchema
from services import city_svc

router = APIRouter()


@router.get("/external-fetching", response_model=List[FetchCitySchema])
async def fetch_cities():
    return city_svc.fetch_cities()


@router.get("/external-fetching/save", response_model=FetchSaveCitySchema)
async def fetch_cities_and_save(db: AsyncSession = Depends(get_db_session)):
    created_qty, updated_qty = await city_svc.fetch_and_save_cities(db)
    return {"message": "Fetching and saving completed", "created_qty": created_qty, "updated_qty": updated_qty}


@router.get("", response_model=List[GetCitySchema])
async def list_cities(
    ids: str = None, name: str = None, state_abbreviation: str = None, db: AsyncSession = Depends(get_db_session)
):
    if ids:
        ids = ids.split(",")
    return await city_svc.get_cities(db, ids, name, state_abbreviation)


@router.get("/{id}", response_model=GetCitySchema)
async def get_city_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    return await city_svc.get_city_by_id(db, id)
