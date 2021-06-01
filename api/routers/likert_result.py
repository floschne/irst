from typing import List

from fastapi import APIRouter, Depends
from loguru import logger
from starlette.responses import JSONResponse

from backend.study import LikertStudyCoordinator
from backend.auth import JWTBearer
from backend.db import RedisHandler
from models.likert_result import LikertResult

PREFIX = "/likert_result"
TAG = ["likert_result"]

router = APIRouter()

redis = RedisHandler()
sc = LikertStudyCoordinator()


@logger.catch(reraise=True)
@router.get("/list", tags=TAG,
            response_model=List[LikertResult],
            description="Returns all submitted LikertResults",
            dependencies=[Depends(JWTBearer())])
async def list_ranking_results():
    logger.info(f"GET request on {PREFIX}/list")
    return redis.list_ranking_results()


@logger.catch(reraise=True)
@router.get("/{lr_id}", tags=TAG,
            response_model=LikertResult,
            description="Returns the LikertResult with the specified ID",
            dependencies=[Depends(JWTBearer())])
async def load(lr_id: str):
    logger.info(f"GET request on {PREFIX}/{lr_id}")
    return redis.load_ranking_result(lr_id)


@logger.catch(reraise=True)
@router.put("/submit", tags=TAG,
            description="Submit a LikertResult",
            dependencies=[Depends(JWTBearer(admin_only=False))])
async def submit(result: LikertResult):
    logger.info(f"GET request on {PREFIX}/submit")
    return JSONResponse(content=sc.submit(result))
