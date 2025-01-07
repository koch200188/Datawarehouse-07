from pydantic import BaseModel
from datetime import datetime

class DistrictSchema(BaseModel):
    districtCode: int
    districtName: str

class DateSchema(BaseModel):
    date: datetime
    year: int
    month: int
    day: int

class ElectionFactSchema(BaseModel):
    districtCode: int
    date: datetime
    övpVotes: int
    spöVotes: int
    fpöVotes: int
    grüneVotes: int
    neosVotes: int
    otherVotes: int

class WeatherFactSchema(BaseModel):
    districtCode: int
    date: datetime
    airPressure: float
    temperature: float
    humidity: float
    wind: float
    rainfall: float