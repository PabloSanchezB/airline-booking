from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.db import Base
from app.catalog.models import Flight
from app.user.models import User

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(20))
    outbound_flight_id = Column(Integer, ForeignKey(Flight.id, ondelete="CASCADE"))
    outbound_flight = relationship("Flight", back_populates="bookings")
    payment_token = Column(String(50))
    checked_in = Column(Boolean)
    customer_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    customer = relationship("User", back_populates="bookings")
    created_at = Column(String(50))
    booking_reference = Column(String(50))
