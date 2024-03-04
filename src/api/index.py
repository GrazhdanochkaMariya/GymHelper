from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Home"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_user():
    return {"index": "HomePage"}