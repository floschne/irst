from typing import List

from fastapi import APIRouter, Depends
from loguru import logger
from starlette.responses import JSONResponse

from backend.auth import JWTBearer
from backend.db import RedisHandler
from backend.study import RatingWithFocusStudyCoordinator
from models import RatingWithFocusResult

PREFIX = "/rating_with_focus_result"
TAG = ["rating_with_focus_result"]

router = APIRouter()

redis = RedisHandler()


@logger.catch(reraise=True)
@router.get("/list", tags=TAG,
            response_model=List[RatingWithFocusResult],
            description="Returns all submitted RatingWithFocusResults",
            dependencies=[Depends(JWTBearer())])
async def list_rating_with_focus_results():
    logger.info(f"GET request on {PREFIX}/list")
    return redis.list_rating_with_focus_results()


@logger.catch(reraise=True)
@router.get("/{rr_id}", tags=TAG,
            response_model=RatingWithFocusResult,
            description="Returns the RatingWithFocusResult with the specified ID",
            dependencies=[Depends(JWTBearer())])
async def load(rr_id: str):
    logger.info(f"GET request on {PREFIX}/{rr_id}")
    return redis.load_rating_with_focus_result(rr_id)


@logger.catch(reraise=True)
@router.put("/submit", tags=TAG,
            description="Submit a RatingWithFocusResult",
            dependencies=[Depends(JWTBearer(admin_only=False))])
async def submit(result: RatingWithFocusResult):
    logger.info(f"GET request on {PREFIX}/submit")
    sc = RatingWithFocusStudyCoordinator()
    return JSONResponse(content=sc.submit(result))
