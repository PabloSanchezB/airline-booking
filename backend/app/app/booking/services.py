from typing import List, Optional
from sqlalchemy.orm import Session
from . import models
from . import schema
from app.user.models import User

async def get_booking_by_id(booking_id:int, db_session:Session) -> models.Booking:
    booking = db_session.query(models.Booking).get(booking_id)
    return booking


def get_user_ids_by_name(customerName:str, db_session: Session) -> List[int]:
    users = db_session.query(User).filter(User.name == customerName).all()
    return [user.id for user in users]

async def search_bookings(status:Optional[schema.BookingStatus], customerName:Optional[str], 
                          db_session: Session) -> List[models.Booking]:
    if customerName:
        ids = get_user_ids_by_name(customerName, db_session)
        if ids and status:
            return db_session.query(models.Booking).filter(models.Booking.customer_id.in_(ids),
                                                           models.Booking.status == status.value).all()
        if ids:
            return db_session.query(models.Booking).filter(models.Booking.customer_id.in_(ids)).all()
        return []
    if status:
        return db_session.query(models.Booking).filter(models.Booking.status == status.value).all()
    return db_session.query(models.Booking).all()

async def create_new_booking(flight_id:int, user_id:int, booking_in: schema.BookingCreate, db_session: Session) -> models.Booking:
    new_booking = models.Booking(status=booking_in.status.value, 
                                 outbound_flight_id=flight_id,
                                 payment_token=booking_in.payment_token, 
                                 checked_in=booking_in.checked_in,
                                 customer_id=user_id,
                                 created_at=booking_in.created_at,
                                 booking_reference=booking_in.booking_reference)

    db_session.add(new_booking)
    db_session.commit()
    db_session.refresh(new_booking)
    return new_booking

async def delete_booking_by_id(booking_id:int, db_session:Session): 
    db_session.query(models.Booking).filter(models.Booking.id == booking_id).delete()
    db_session.commit()

async def get_booking_by_flight(flight_id:int, db_session: Session) -> List[models.Booking]:
    return db_session.query(models.Booking).filter(models.Booking.outbound_flight_id == flight_id).all()


