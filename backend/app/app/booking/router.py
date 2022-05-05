from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List
from app.database import db
from . import schema
from . import services
from . import validation

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bookings found")
    return bookings
