from typing import Optional

from sqlalchemy.orm import Session

from app.catalog.models import Flight
from app.user.models import User


async def verify_flight_exist(flight_id: int, db_session: Session) -> Optional[Flight]:
    return db_session.query(Flight).filter(Flight.id == flight_id).first()

async def verify_user_exist(user_id: int, db_session: Session) -> Optional[User]:
    return db_session.query(User).filter(User.id == user_id).first()