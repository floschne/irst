from typing import List

from fastapi import APIRouter, Depends
from loguru import logger
from starlette.responses import JSONResponse

from backend.study import RatingStudyCoordinator
from backend.auth import JWTBearer
from backend.db import RedisHandler
from models import RatingResult

PREFIX = "/rating_result"
TAG = ["rating_result"]

router = APIRouter()

redis = RedisHandler()


@logger.catch(reraise=True)
@router.get("/list", tags=TAG,
            response_model=List[RatingResult],
            description="Returns all submitted RatingResults",
            dependencies=[Depends(JWTBearer())])
async def list_rating_results():
    logger.info(f"GET request on {PREFIX}/list")
    return redis.list_rating_results()


@logger.catch(reraise=True)
@router.get("/{rr_id}", tags=TAG,
            response_model=RatingResult,
            description="Returns the RatingResult with the specified ID",
            dependencies=[Depends(JWTBearer())])
async def load(rr_id: str):
    logger.info(f"GET request on {PREFIX}/{rr_id}")
    return redis.load_rating_result(rr_id)


@logger.catch(reraise=True)
@router.put("/submit", tags=TAG,
            description="Submit a RatingResult",
            dependencies=[Depends(JWTBearer(admin_only=False))])
async def submit(result: RatingResult):
    logger.info(f"GET request on {PREFIX}/submit")
    sc = RatingStudyCoordinator()
    return JSONResponse(content=sc.submit(result))
