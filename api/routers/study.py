from fastapi import APIRouter, Depends
from loguru import logger

from backend import StudyCoordinator
from backend.auth import JWTBearer

PREFIX = "/study"
TAG = ["study"]

router = APIRouter()


@logger.catch(reraise=True)
@router.get("/progress", tags=TAG,
            description="Returns the current progress of the Study",
            dependencies=[Depends(JWTBearer())])
async def get_progress():
    logger.info(f"GET request on {PREFIX}/progress")
    return StudyCoordinator().current_progress()
