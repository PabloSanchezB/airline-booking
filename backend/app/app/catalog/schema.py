from pydantic import BaseModel
from datetime import datetime, date

class FlightBase(BaseModel):
    departure_date: date
    departure_airport_code: str
    departure_airport_name: str
    departure_city: str
    departure_locale: str
    arrival_date: date
    arrival_airport_code: str
    arrival_airport_name: str
    arrival_city: str
    arrival_locale: str
    ticket_price: int
    ticket_currency: str
    flight_number: int
    seat_capacity: int

class FlightCreate(FlightBase):
    pass

class FlightUpdate(FlightBase):
    pass

class FlightInDBBase(FlightBase):
    id: int

    class Config:
        orm_mode = True

class Flight(FlightInDBBase):
    pass

class FlightInDB(FlightInDBBase):
    pass