from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class District(Base):
    __tablename__ = "district"
    district_code = Column(Integer, primary_key=True, autoincrement=False)
    district_name = Column(String(100))

class Date(Base):
    __tablename__ = "date"
    date = Column(TIMESTAMP, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)

class ElectionFact(Base):
    __tablename__ = "election_fact"
    district_code = Column(Integer, ForeignKey("district.district_code"), nullable=False)
    date = Column(TIMESTAMP, ForeignKey("date.date"), nullable=False)
    övp_votes = Column(Integer)
    spö_votes = Column(Integer)
    fpö_votes = Column(Integer)
    grüne_votes = Column(Integer)
    neos_votes = Column(Integer)
    other_votes = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint("district_code", "date"),
    )

class WeatherFact(Base):
    __tablename__ = "weather_fact"
    district_code = Column(Integer, ForeignKey("district.district_code"), nullable=False)
    date = Column(TIMESTAMP, ForeignKey("date.date"), nullable=False)
    air_pressure = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    wind = Column(Float)
    rainfall = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint("district_code", "date"),
    )