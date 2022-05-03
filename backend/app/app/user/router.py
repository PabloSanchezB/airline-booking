from typing import Any, List

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from app.database import db

from . import schema
from . import services
from . import validator

api_router = APIRouter(tags=['Users'])

@api_router.get('/users/{user_id}', response_model=schema.User)
async def get_user_by_id(user_id: int, db_session: Session = Depends(db.get_db)):
    return await services.get_user_by_id(user_id, db_session)

@api_router.get('/users/', response_model=List[schema.User])
async def get_all_users(db_session: Session = Depends(db.get_db)):
    return await services.all_users(db_session)

@api_router.post('/users/', status_code=status.HTTP_201_CREATED, response_model=schema.User)
async def create_user_registration(user_in: schema.UserCreate, db_session: Session = Depends(db.get_db)):

    user = await validator.verify_email_exist(user_in.email, db_session)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system."
        )

    new_user = await services.new_user_register(user_in, db_session)
    return new_user

@api_router.put("/users/{user_id}", response_model = schema.User)
async def update_user_by_id(user_id:int, user_in: schema.UserUpdate, db_session: Session = Depends(db.get_db)) -> Any:
    user= await services.get_user_by_id(user_id, db_session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user ID")
    
    user2 = await validator.verify_email_exist(user_in.email, db_session)
    if user2 and user2.id != user_id:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system."
        )
    
    await services.update_user_by_id(user_id, user_in, db_session)

    return await services.get_user_by_id(user_id, db_session)

@api_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id:int, db_session: Session = Depends(db.get_db)):
    user= await services.get_user_by_id(user_id, db_session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user ID")
    
    return await services.delete_user_by_id(user_id, db_session)

