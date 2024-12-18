from pydantic import BaseModel
from datetime import datetime


class Location(BaseModel):
    districtCode: int
    date: datetime
    districtName: str

class PopulationData(BaseModel):
    districtCode: int
    date: datetime
    austrianCitizens: int
    foreignCitizens: int

class EducationData(BaseModel):
    districtCode: int
    date: datetime
    academicEducation: float
    statutoryEducation: float
    highschoolEducation: float
    vocationalEducation: float
    
class ElectionData(BaseModel):
    districtCode: int
    date: datetime
    oevpVotes: int
    spoeVotes: int
    fpoeVotes: int
    grueneVotes: int
    neosVotes: int
    otherVotes: int

class WeatherData(BaseModel):
    districtCode: int
    date: datetime
    airPressure: float
    temperature: float
    humidity: float
    wind: float
    rainfall: float
    