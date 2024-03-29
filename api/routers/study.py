from fastapi import APIRouter, Depends
from loguru import logger

from backend.study import LikertStudyCoordinator, RankingStudyCoordinator
from backend.auth import JWTBearer

PREFIX = "/study"
TAG = ["study"]

router = APIRouter()


@logger.catch(reraise=True)
@router.get("/progress", tags=TAG,
            description="Returns the current progress of the Study",
            dependencies=[Depends(JWTBearer())])
async def get_progress(study_type: str):
    logger.info(f"GET request on {PREFIX}/progress")
    coords = {'likert': LikertStudyCoordinator(),
              'ranking': RankingStudyCoordinator()}
    return coords[study_type].current_progress()
