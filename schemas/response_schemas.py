from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FetchCitySchema(BaseModel):
    name: str
    state_abbreviation: str


class GetCitySchema(BaseModel):
    id: int
    name: str
    state_abbreviation: str
    created: datetime
    updated: Optional[datetime]


class FetchSaveCitySchema(BaseModel):
    message: str
    created_qty: int
    updated_qty: int
