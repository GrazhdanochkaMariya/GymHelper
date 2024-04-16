from fastapi import APIRouter, Request, Depends

from src.api.api_dependencies import db_dependency, get_current_user, templates
from src.crud.exercise import ExerciseCRUD
from src.crud.user_measurements import UserMeasurementsCRUD
from src.crud.workout import WorkoutCRUD
from src.models import User

router = APIRouter(prefix="/pages", tags=["Pages"])


@router.get("/base")
async def get_base_page(request: Request):
    user = request.session.get("token")
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@router.get("/signup")
async def get_registration_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.get("/login")
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/user/")
async def get_user_profile_page(
    request: Request, user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "user_profile.html", {"request": request, "user": user}
    )


@router.get("/workouts/")
async def get_users_workouts(
    request: Request, session: db_dependency, user: User = Depends(get_current_user)
):
    workouts = await WorkoutCRUD(session).select_users_workouts_by_user_id(
        user_id=user.id
    )
    return templates.TemplateResponse(
        "user_workouts.html", {"request": request, "workouts": workouts, "user": user}
    )


@router.get("/exercises/{workout_id}")
async def get_workout_exercise(
    request: Request,
    workout_id: int,
    session: db_dependency,
    user: User = Depends(get_current_user),
):
    exercises = await ExerciseCRUD(session).select_all_filter_by(workout_id=workout_id)
    return templates.TemplateResponse(
        "workouts_exercises.html",
        {"request": request, "exercises": exercises, "user": user},
    )


@router.get("/add-exercise/{workout_id}")
async def get_create_exercise_page(
    request: Request, user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "create_workout_exercise.html", {"request": request}
    )


@router.get("/measurements/")
async def get_users_measurements(
    request: Request, session: db_dependency, user: User = Depends(get_current_user)
):
    user_measurements = await UserMeasurementsCRUD(session).select_all_filter_by(
        user_id=user.id
    )
    return templates.TemplateResponse(
        "user_measurements.html",
        {"request": request, "measurements": user_measurements, "user": user},
    )


@router.get("/plots/")
async def get_measurements_plots(
    request: Request, session: db_dependency, user: User = Depends(get_current_user)
):
    user_measurements = await UserMeasurementsCRUD(session).select_all_filter_by(
        user_id=user.id
    )
    user_data = [
        (measurement.created_at.strftime("%Y-%m-%d %H:%M"), measurement.weight)
        for measurement in user_measurements
    ]
    return templates.TemplateResponse(
        "user_measurements_plots.html",
        {
            "request": request,
            "measurements": user_measurements,
            "user": user,
            "user_data": user_data,
        },
    )


@router.get("/add-measurement/{user_id}")
async def get_create_measurement_page(
    request: Request, user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "create_user_measurement.html", {"request": request, "user": user}
    )


@router.get("/add-workout/")
async def get_create_workout_page(
    request: Request, user: User = Depends(get_current_user)
):
    # TODO include library with calendar
    return templates.TemplateResponse(
        "create_workout.html", {"request": request, "user": user}
    )
