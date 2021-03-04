from fastapi import APIRouter
from loguru import logger

from backend import StudyCoordinator

PREFIX = "/study"
TAG = ["study"]

router = APIRouter()


@logger.catch(reraise=True)
@router.get("/progress", tags=TAG,
            description="Returns the current progress of the Study")
async def get_progress():
    logger.info(f"GET request on {PREFIX}/progress")
    return StudyCoordinator().current_progress()
