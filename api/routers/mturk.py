from fastapi import APIRouter, Depends
from loguru import logger

from backend.auth import AuthHandler, JWTBearer
from backend.db import RedisHandler
from backend.mturk import MTurkHandler

PREFIX = "/mturk"
TAG = ["mturk"]

router = APIRouter()

mturk = MTurkHandler()
rh = RedisHandler()


@logger.catch(reraise=True)
@router.post("/create_hit", tags=TAG,
             description="Returns the current progress of the Study",
             dependencies=[Depends(JWTBearer())])
async def create_hit(es_id: str):
    logger.info(f"GET request on {PREFIX}/create_hit")
    es = rh.load_eval_sample(sample_id=es_id)
    if es is not None:
        return mturk.create_hit_from_es(es)
