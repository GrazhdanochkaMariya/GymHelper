from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.auth import router as auth_router
from src.api.user import router as user_router
from src.api.user_measurements import router as user_measurements_router
from src.api.workout import router as workout_router
from src.api.exercise import router as exercise_router
from src.pages.pages import router as pages_router

from config import app_configs, settings

app = FastAPI(**app_configs)

app.mount("/static", StaticFiles(directory="src/static"), name="static")


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(user_measurements_router)
app.include_router(workout_router)
app.include_router(pages_router)
app.include_router(exercise_router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    https_only=settings.MODE == "production",
)
