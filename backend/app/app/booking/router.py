from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from app.database import db
from . import schema
from . import services
from . import validator
from app.core import security 
from app.user import schema as user_schema

api_router = APIRouter(tags=["Booking"])

@api_router.get("/booking/{booking_id}", response_model=schema.Booking)
async def get_booking_by_id(booking_id:int, db_session: Session = Depends(db.get_db)):
    booking= await services.get_booking_by_id(booking_id, db_session)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    
    return booking

@api_router.get("/booking/", response_model=List[schema.Booking])
async def search_bookings(status:Optional[schema.BookingStatus]=None, customerName:Optional[str]=None,
                          db_session: Session = Depends(db.get_db)):
    bookings = await services.search_bookings(status, customerName, db_session)
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found")
    return bookings

@api_router.post("/booking/flight/{flight_id}/user/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_booking(flight_id:int, user_id:int, booking_in: schema.BookingCreate, 
                         db_session: Session = Depends(db.get_db),
                         current_user: user_schema.User = Depends(security.get_current_user)):
    flight = await validator.verify_flight_exist(flight_id, db_session)
    if not flight:
        raise HTTPException(status_code=404, detail="You have provided invalid flight id.")
    
    user = await validator.verify_user_exist(user_id, db_session)
    if not user:
        raise HTTPException(status_code=404, detail="You have provided invalid user id.")

    booking = await services.create_new_booking(flight_id, user_id, booking_in, db_session)
    return booking

@api_router.delete("/booking/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking_by_id(booking_id:int, db_session: Session = Depends(db.get_db),
                               current_user: user_schema.User = Depends(security.get_current_user)):
    booking= await services.get_booking_by_id(booking_id, db_session)
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid booking ID")
    
    return await services.delete_booking_by_id(booking_id, db_session)

@api_router.get("/booking/flight/{flight_id}", response_model=List[schema.Booking])
async def get_booking_by_flight(flight_id:int, db_session: Session = Depends(db.get_db)):
    bookings = await services.get_booking_by_flight(flight_id, db_session)
    if not bookings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bookings found")
    return bookings


