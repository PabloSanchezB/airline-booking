from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models
from . import schema
from app.core import hashing

async def get_user_by_id(user_id: int, db_session: Session) -> Optional[models.User]:
    user_info = db_session.query(models.User).get(user_id)
    #if not user_info:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found !")
    return user_info

async def all_users(db_session: Session) -> List[models.User]:
    users = db_session.query(models.User).all()
    return users

