from pydantic import BaseModel
from enum import Enum
from app.catalog.schema import Flight
from app.user.schema import User

class BookingStatus(str, Enum):
    UNCONFIRMED = 'UNCONFIRMED'
    CONFIRMED = 'CONFIRMED'
    CANCELLED = 'CANCELLED'

class BookingBase(BaseModel):
    status: BookingStatus
    payment_token: str
    checked_in: bool
    created_at: str
    booking_reference: str

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BookingBase):
    pass

class BookingInDBBase(BookingBase):
    id: int
    outbound_flight_id: int
    outbound_flight: Flight
    customer_id: int
    customer: User

    class Config:
        orm_mode = True

class Booking(BookingInDBBase):
    pass

class BookingInDB(BookingInDBBase):
    pass

