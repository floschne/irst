from typing import List

from fastapi import APIRouter, Depends
from loguru import logger

from backend.auth import JWTBearer
from backend.db import RedisHandler
from models import ModelRanking

PREFIX = "/mranking"
TAG = ["mranking"]
router = APIRouter()

rh = RedisHandler()


@logger.catch(reraise=True)
@router.get("/list", tags=TAG,
            response_model=List[ModelRanking],
            description="Returns all ModelRankings",
            dependencies=[Depends(JWTBearer())])
async def list_rankings(num: int = 100):
    logger.info(f"GET request on {PREFIX}/list")
    return rh.list_model_rankings(num)


@logger.catch(reraise=True)
@router.get("/{mr_id}", tags=TAG,
            response_model=ModelRanking,
            description="Returns the ModelRanking with the specified ID",
            dependencies=[Depends(JWTBearer())])
async def load_ranking(mr_id: str):
    logger.info(f"GET request on {PREFIX}/{mr_id}")
    return rh.load_model_ranking(mr_id)
