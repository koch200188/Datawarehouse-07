from db.session import SessionLocal
from sqlalchemy import func
from datetime import datetime
from db.model import District, Date, ElectionFact, WeatherFact
from api.model import DistrictSchema, DateSchema, ElectionFactSchema, WeatherFactSchema

def read_district(district_code: int, db: Session):
    return db.query(District).filter(District.districtCode == district_code).first()

def read_all_districts(skip: int = 0, limit: int = 100):
    return SessionLocal.query(District).offset(skip).limit(limit).all()

def read_date(date: datetime, db: Session):
    return db.query(Date).filter(Date.date == date).first()

def read_all_dates(skip: int = 0, limit: int = 100, db: Session):
    return db.query(Date).offset(skip).limit(limit).all()

def read_election_fact(district_code: int, date: datetime, db: Session):
    return db.query(ElectionFact).filter(
        ElectionFact.districtCode == district_code,
        ElectionFact.date == date
    ).first()

def read_all_election_facts(skip: int = 0, limit: int = 100, db: Session):
    return db.query(ElectionFact).offset(skip).limit(limit).all()

def read_weather_fact(district_code: int, date: datetime, db: Session):
    return db.query(WeatherFact).filter(
        WeatherFact.districtCode == district_code,
        WeatherFact.date == date
    ).first()

def read_all_weather_facts(skip: int = 0, limit: int = 100, db: Session):
    return db.query(WeatherFact).offset(skip).limit(limit).all()

def read_total_votes_by_party(db: Session):
    return db.query(
        func.sum(ElectionFact.övpVotes).label("övp_total"),
        func.sum(ElectionFact.spöVotes).label("spö_total"),
        func.sum(ElectionFact.fpöVotes).label("fpö_total"),
        func.sum(ElectionFact.grüneVotes).label("grüne_total"),
        func.sum(ElectionFact.neosVotes).label("neos_total"),
        func.sum(ElectionFact.otherVotes).label("other_total")
    ).first()

def read_average_temperature_by_district(db: Session):
    return db.query(
        WeatherFact.districtCode,
        func.avg(WeatherFact.temperature).label("avg_temperature")
    ).group_by(WeatherFact.districtCode).all()

def read_election_results_with_weather(district_code: int, date: str, db: Session):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    election_result = read_election_fact(district_code, date_obj, db)
    weather = read_weather_fact(district_code, date_obj, db)
    return election_result, weather

def read_election_trends(start_date: str, end_date: str, db: Session):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return db.query(
        ElectionFact.date,
        func.sum(ElectionFact.övpVotes).label("övp_votes"),
        func.sum(ElectionFact.spöVotes).label("spö_votes"),
        func.sum(ElectionFact.fpöVotes).label("fpö_votes"),
        func.sum(ElectionFact.grüneVotes).label("grüne_votes"),
        func.sum(ElectionFact.neosVotes).label("neos_votes"),
        func.sum(ElectionFact.otherVotes).label("other_votes")
    ).filter(ElectionFact.date.between(start, end)).group_by(ElectionFact.date).order_by(ElectionFact.date).all()

def read_weather_impact_on_voting(db: Session):
    return db.query(
        WeatherFact.temperature,
        func.sum(ElectionFact.övpVotes + ElectionFact.spöVotes + ElectionFact.fpöVotes + 
                 ElectionFact.grüneVotes + ElectionFact.neosVotes + ElectionFact.otherVotes).label("total_votes")
    ).join(ElectionFact, (WeatherFact.districtCode == ElectionFact.districtCode) & 
                         (WeatherFact.date == ElectionFact.date)
    ).group_by(WeatherFact.temperature).order_by(WeatherFact.temperature).all()
