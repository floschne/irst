from fastapi import APIRouter, Depends
from loguru import logger

from backend.auth import JWTBearer
from backend.db import RedisHandler
from backend.mturk import MTurkHandler

PREFIX = "/mturk"
TAG = ["mturk"]

router = APIRouter()

mturk = MTurkHandler()
rh = RedisHandler()


@logger.catch(reraise=True)
@router.put("/create_hit", tags=TAG,
            description="Creates a HIT for the EvalSample with the given ES ID",
            dependencies=[Depends(JWTBearer())])
async def create_hit(es_id: str):
    logger.info(f"POST request on {PREFIX}/create_hit")
    es = rh.load_eval_sample(sample_id=es_id)
    if es is not None:
        return mturk.create_hit_from_es(es)
    return False


@logger.catch(reraise=True)
@router.delete("/delete_hit", tags=TAG,
               description="Deletes the HIT with the given ID",
               dependencies=[Depends(JWTBearer())])
async def delete_hit(hit_id: str):
    logger.info(f"DELETE request on {PREFIX}/delete_hit")
    return mturk.delete_hit(hit_id)


@logger.catch(reraise=True)
@router.get("/list_hit_ids", tags=TAG,
            description="Returns all HIT IDs",
            dependencies=[Depends(JWTBearer())])
async def list_hit_ids():
    logger.info(f"GET request on {PREFIX}/list_hit_ids")
    return mturk.list_hit_ids()


@logger.catch(reraise=True)
@router.get("/hit_info/{es_id}", tags=TAG,
            description="Returns the HIT Info of associated with the given EvalSample ID",
            dependencies=[Depends(JWTBearer())])
async def hit_info(es_id: str):
    logger.info(f"GET request on {PREFIX}/hit_info/{es_id}")
    es = rh.load_eval_sample(sample_id=es_id)
    if es is not None:
        return mturk.get_hit_info(es)
    return False
