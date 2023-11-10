from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db_session
from schemas.response_schemas import FetchCitySchema, GetCitySchema
from services import city_svc

app = FastAPI()


@app.get("/")
async def status():
    """
    This endpoint is used for health metrics
    """
    return {"status": "ok"}


@app.get("/city/external-fetching", response_model=List[FetchCitySchema])
async def fetch_cities():
    """
    This route is used for fetching all existing cities in Brazil through IBGE's API
    """
    return city_svc.fetch_cities()


@app.get("/city/external-fetching/save", response_model=List[GetCitySchema])
async def fetch_cities_and_save(db: AsyncSession = Depends(get_db_session)):
    """
    This route is used for fetching all existing cities in Brazil through IBGE's API and saving them on database
    """
    return await city_svc.fetch_and_save_cities(db)


@app.get("/city", response_model=List[GetCitySchema])
async def list_cities(ids: str = None, name: str = None, state_abbreviation: str = None, db: AsyncSession = Depends(get_db_session)):
    """
    This route is used to list persisted cities
    """
    if ids:
        ids = ids.split(",")
    return await city_svc.get_cities(db, ids, name, state_abbreviation)


@app.get("/city/{id}", response_model=GetCitySchema)
async def list_cities(id: int, db: AsyncSession = Depends(get_db_session)):
    """
    This route is used to list persisted cities
    """
    return await city_svc.get_city_by_id(db, id)
