from typing import List

from fastapi import APIRouter, Depends
from loguru import logger
from starlette.responses import JSONResponse

from backend import StudyCoordinator
from backend.auth import JWTBearer
from backend.db import RedisHandler
from models import RankingResult

PREFIX = "/ranking_result"
TAG = ["ranking_result"]

router = APIRouter()

redis = RedisHandler()
sc = StudyCoordinator()


@logger.catch(reraise=True)
@router.get("/list", tags=TAG,
            response_model=List[RankingResult],
            description="Returns all submitted RankingResults",
            dependencies=[Depends(JWTBearer())])
async def list_ranking_results():
    logger.info(f"GET request on {PREFIX}/list")
    return redis.list_ranking_results()


@logger.catch(reraise=True)
@router.get("/{rr_id}", tags=TAG,
            response_model=RankingResult,
            description="Returns the RankingResult with the specified ID",
            dependencies=[Depends(JWTBearer())])
async def load(rr_id: str):
    logger.info(f"GET request on {PREFIX}/{rr_id}")
    return redis.load_ranking_result(rr_id)


@logger.catch(reraise=True)
@router.put("/submit", tags=TAG,
            description="Submit an RankingResult")
async def submit(result: RankingResult):
    logger.info(f"GET request on {PREFIX}/submit")
    return JSONResponse(content=sc.submit(result))
