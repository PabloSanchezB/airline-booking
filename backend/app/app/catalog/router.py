from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from app.database import db
from . import schema
from . import services
#from . import validation
#from app.core import security #Para importar la seguridad
#from app.user import schema as user_schema
from datetime import datetime, date

api_router = APIRouter(tags=["Catalog"])

@api_router.get("/catalog/", response_model=List[schema.Flight])
async def search_catalog(departureAirportCode:Optional[str]=None, arrivalAirportCode:Optional[str]=None,
                         departureDate:Optional[str]=None, db_session: Session = Depends(db.get_db)):
    probDate = None
    if departureDate:
        try:
            probDate = datetime.strptime(departureDate, '%Y-%m-%d').date()
        except:
            raise HTTPException(status_code=400, detail="Invalid date. Date must be year-month-day. E.g. 1997-08-16")

    flights = await services.search_catalog(departureAirportCode, arrivalAirportCode, probDate, db_session)
    if not flights:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No flights found")
    return flights

@api_router.post("/catalog/", status_code=status.HTTP_201_CREATED)
async def create_flight(flight_in: schema.FlightCreate, db_session: Session = Depends(db.get_db)) -> Any:
    flight = await services.create_flight(flight_in, db_session)
    return flight
    

