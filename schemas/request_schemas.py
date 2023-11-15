from pydantic import BaseModel, Field

from database.models import CityLogStatus


class CreateLogSchema(BaseModel):
    city_id: int = Field(alias="cityId")
    status: CityLogStatus
