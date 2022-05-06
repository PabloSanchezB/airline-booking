from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from app.database import db
from . import schema
from . import services
from app.core import security 
from app.user import schema as user_schema
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
async def create_flight(flight_in: schema.FlightCreate, db_session: Session = Depends(db.get_db),
                        current_user: user_schema.User = Depends(security.get_current_user)) -> Any:
    flight = await services.create_flight(flight_in, db_session)
    return flight

@api_router.put("/catalog/{flight_id}")
async def update_flight_by_id(flight_id:int, flight_in: schema.FlightUpdate, 
                              db_session: Session = Depends(db.get_db),
                              current_user: user_schema.User = Depends(security.get_current_user)) -> Any:
    flight= await services.get_flight_by_id(flight_id, db_session)
    if not flight:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid flight ID")
    
    await services.update_flight_by_id(flight_id, flight_in, db_session)

    return await services.get_flight_by_id(flight_id, db_session)

@api_router.delete("/catalog/{flight_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flight_by_id(flight_id:int, db_session: Session = Depends(db.get_db),
                              current_user: user_schema.User = Depends(security.get_current_user)):
    flight= await services.get_flight_by_id(flight_id, db_session)
    if not flight:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid flight ID")
    
    return await services.delete_flight_by_id(flight_id, db_session)

@api_router.get("/catalog/{airportCode}", response_model=List[schema.Flight])
async def search_airport_depart(airportCode: str, departureDate: str, db_session: Session = Depends(db.get_db)):
    probDate = None
    try:
        probDate = datetime.strptime(departureDate, '%Y-%m-%d').date()
    except:
        raise HTTPException(status_code=400, detail="Invalid date. Date must be year-month-day. E.g. 1997-08-16")
    
    flights = await services.search_airport_depart(airportCode, probDate, db_session)
    if not flights:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No flights found")
    return flights



