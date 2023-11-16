from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import CityLogStatus
from database.session import get_db_session
from schemas.request_schemas import CreateLogSchema
from schemas.response_schemas import CityLogSchema, FetchCitySchema, FetchSaveCitySchema, GetCitySchema
from services import city_svc

router = APIRouter()


@router.get("/external-fetching", response_model=List[FetchCitySchema])
async def fetch_cities():
    return city_svc.fetch_cities()


@router.post("/external-fetching/save", response_model=FetchSaveCitySchema)
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


@router.get("/{id:int}", response_model=GetCitySchema)
async def get_city_by_id(id: int, db: AsyncSession = Depends(get_db_session)):
    return await city_svc.get_city_by_id(db, id)


@router.post("/log", response_model=CityLogSchema)
async def create_city_log(item: CreateLogSchema, db: AsyncSession = Depends(get_db_session)):
    return await city_svc.create_city_log(db, item.city_id, item.status)


@router.get("/log", response_model=List[CityLogSchema])
async def get_city_log(
    ids: str = None, city_id: int = None, status: str = None, db: AsyncSession = Depends(get_db_session)
):
    if ids:
        ids = ids.split(",")
    return await city_svc.get_city_log(db, ids, city_id, status)


@router.get("/log/most-recent-selected-cities", response_model=List[GetCitySchema])
async def get_most_recent_selected_cities(db: AsyncSession = Depends(get_db_session)):
    return await city_svc.get_most_recent_selected_cities(db, status=CityLogStatus.SELECTED)
