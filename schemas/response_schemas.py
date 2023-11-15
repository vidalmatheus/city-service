from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from database.models import CityLogStatus


class FetchCitySchema(BaseModel):
    name: str
    state_abbreviation: str


class GetCitySchema(BaseModel):
    id: int
    name: str
    state_abbreviation: str
    created_at: datetime
    updated_at: Optional[datetime]


class FetchSaveCitySchema(BaseModel):
    message: str
    created_qty: int
    updated_qty: int


class CityLogSchema(BaseModel):
    id: int
    city: GetCitySchema
    status: CityLogStatus
    created_at: datetime
