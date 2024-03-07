from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.api.auth import router as auth_router
from src.api.user import router as user_router
from src.api.user_measurements import router as user_measurements_router
from src.api.workout import router as workout_router

from config import app_configs, settings

app = FastAPI(**app_configs)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(user_measurements_router)
app.include_router(workout_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    https_only=settings.MODE == "production",
)
