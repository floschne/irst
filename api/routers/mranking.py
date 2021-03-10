from fastapi import APIRouter
from loguru import logger

from backend.db import RedisHandler
from models import ModelRanking

PREFIX = "/mranking"
TAG = ["mranking"]
router = APIRouter()

redis = RedisHandler()


@logger.catch(reraise=True)
@router.get("/{mr_id}", tags=TAG,
            response_model=ModelRanking,
            description="Returns the ModelRanking with the specified ID")
async def load_sample(mr_id: str):
    logger.info(f"GET request on {PREFIX}/{mr_id}")
    return redis.load_model_ranking(mr_id)
