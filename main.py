from fastapi import FastAPI

from src.api.auth import router as auth_router
from src.api.user import router as user_router
from src.api.user_measurements import router as user_measurements_router

from config import app_configs

app = FastAPI(**app_configs)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(user_measurements_router)
