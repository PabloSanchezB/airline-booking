from fastapi import FastAPI
from app.core import config 
from app.catalog import router as catalog_router 
from app.user import router as user_router
from app.booking import router as booking_router
from app.auth import router as auth_router
from app.database import models 

app = FastAPI(title = "Airline Booking App", version = "0.0.1") 

app.include_router(catalog_router.api_router)
app.include_router(user_router.api_router)
app.include_router(booking_router.api_router)
app.include_router(auth_router.api_router)