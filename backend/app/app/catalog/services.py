from typing import List, Optional
from sqlalchemy.orm import Session
from . import models
from . import schema
from datetime import datetime

async def search_catalog(dac:Optional[str], aac:Optional[str], dd:Optional[datetime.date], 
                         db_session: Session) -> List[models.Flight]:
    if dac and aac and dd:
        return db_session.query(models.Flight).filter(models.Flight.departure_airport_code == dac,
                                                      models.Flight.arrival_airport_code == aac,
                                                      models.Flight.departure_date == dd)
    
    if dac and aac:
        return db_session.query(models.Flight).filter(models.Flight.departure_airport_code == dac,
                                                      models.Flight.arrival_airport_code == aac)
    
    if dac and dd:
        return db_session.query(models.Flight).filter(models.Flight.departure_airport_code == dac,
                                                      models.Flight.departure_date == dd)
    
    if aac and dd:
        return db_session.query(models.Flight).filter(models.Flight.arrival_airport_code == aac,
                                                      models.Flight.departure_date == dd)
    
    if dac:
        return db_session.query(models.Flight).filter(models.Flight.departure_airport_code == dac)
    
    if aac:
        return db_session.query(models.Flight).filter(models.Flight.arrival_airport_code == aac)
    
    if dd:
        return db_session.query(models.Flight).filter(models.Flight.departure_date == dd)
    
    return db_session.query(models.Flight).all()