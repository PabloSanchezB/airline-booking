from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship
from app.database.db import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    departure_date = Column(Date)
    departure_airport_code = Column(String(50))
    departure_airport_name = Column(String(50))
    departure_city = Column(String(50))
    departure_locale = Column(String(50))
    arrival_date = Column(Date)
    arrival_airport_code = Column(String(50))
    arrival_airport_name = Column(String(50))
    arrival_city = Column(String(50))
    arrival_locale = Column(String(50))
    ticket_price = Column(Integer)
    ticket_currency = Column(String(50))
    flight_number = Column(Integer)
    seat_capacity = Column(Integer)
    bookings = relationship("Booking", back_populates="outbound_flight")
