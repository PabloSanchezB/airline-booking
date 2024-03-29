from typing import List, Optional
from sqlalchemy.orm import Session
from . import models
from . import schema
from datetime import datetime, date

async def search_catalog(dac:Optional[str], aac:Optional[str], dd:Optional[date], 
                         db_session: Session) -> List[models.Flight]:
    
    if dac and aac and dd:
        return db_session.query(models.Flight).filter(models.Flight.departure_airport_code == dac,
                                                      models.Flight.arrival_airport_code == aac,
                                                      models.Flight.departure_date == dd).all()
    
    if dac and aac:
        return db_session.query(models.Flight).filter(models.Flight.departure_airport_code == dac,
                                                      models.Flight.arrival_airport_code == aac).all()
    
    if dac and dd:
        return db_session.query(models.Flight).filter(models.Flight.departure_airport_code == dac,
                                                      models.Flight.departure_date == dd).all()
    
    if aac and dd:
        return db_session.query(models.Flight).filter(models.Flight.arrival_airport_code == aac,
                                                      models.Flight.departure_date == dd).all()
    
    if dac:
        return db_session.query(models.Flight).filter(models.Flight.departure_airport_code == dac).all()
    
    if aac:
        return db_session.query(models.Flight).filter(models.Flight.arrival_airport_code == aac).all()
    
    if dd:
        return db_session.query(models.Flight).filter(models.Flight.departure_date == dd).all()
    
    return db_session.query(models.Flight).all()

async def create_flight(flight_in: schema.FlightCreate, db_session: Session) -> models.Flight:
    db_flight = models.Flight(**flight_in.dict())
    db_session.add(db_flight)
    db_session.commit()
    db_session.refresh(db_flight)
    return db_flight

async def get_flight_by_id(flight_id:int, db_session:Session) -> models.Flight:
    flight = db_session.query(models.Flight).get(flight_id)
    return flight

async def update_flight_by_id(flight_id:int, flight: schema.FlightUpdate, db_session:Session):
    db_session.query(models.Flight).filter(models.Flight.id == flight_id).update(flight.dict())
    db_session.commit()

async def delete_flight_by_id(flight_id:int, db_session:Session): 
    db_session.query(models.Flight).filter(models.Flight.id == flight_id).delete()
    db_session.commit()

async def search_airport_depart(dac:str, dd:date, db_session:Session) -> List[models.Flight]:
    return db_session.query(models.Flight).filter(models.Flight.departure_airport_code == dac,
                                                  models.Flight.departure_date == dd).all()

