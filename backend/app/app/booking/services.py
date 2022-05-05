from typing import List, Optional
from sqlalchemy.orm import Session
from . import models
from . import schema
from app.user.models import User

async def get_user_ids_by_name(customerName:str, db_session: Session) -> List[int]:
    users = db_session.query(User).filter(User.name == customerName).all()
    return [user.id for user in users]

async def search_bookings(status:Optional[schema.BookingStatus], customerName:Optional[str], 
                          db_session: Session) -> List[models.Booking]:
    if customerName:
        ids = get_user_ids_by_name(customerName, db_session)
        if ids and status:
            return db_session.query(models.Booking).filter(models.Booking.customer_id.in_(ids),
                                                           models.Booking.status == status).all()
        if ids:
            return db_session.query(models.Booking).filter(models.Booking.customer_id.in_(ids)).all()
        return []
    if status:
        return db_session.query(models.Booking).filter(models.Booking.status == status).all()
    return db_session.query(models.Booking).all()


