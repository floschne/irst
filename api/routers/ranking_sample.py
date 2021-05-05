from typing import Union, Optional, List

from fastapi import APIRouter, Depends
from loguru import logger

from backend import StudyCoordinator
from backend.auth import JWTBearer
from backend.db import RedisHandler
from models import RankingSample, MTurkParams

PREFIX = "/ranking_sample"
TAG = ["ranking_sample"]
router = APIRouter()

rh = RedisHandler()
coord = StudyCoordinator()


@logger.catch(reraise=True)
@router.get("/next", tags=TAG,
            response_model=Union[RankingSample, int],
            description="Returns the next RankingSample or the shortest waiting time until the next sample is ready.")
async def get_next_ranking_sample():
    logger.info(f"GET request on {PREFIX}/next")
    return coord.next()


@logger.catch(reraise=True)
@router.get("/list", tags=TAG,
            response_model=List[RankingSample],
            description="Returns all RankingSamples",
            dependencies=[Depends(JWTBearer())])
async def list_ranking_samples(num: int = 100):
    logger.info(f"GET request on {PREFIX}/list")
    return rh.list_ranking_samples(num)


@logger.catch(reraise=True)
@router.get("/{rs_id}", tags=TAG,
            response_model=RankingSample,
            description="Returns the RankingSample with the specified ID")
async def load_sample(rs_id: str, mt: Optional[MTurkParams] = Depends(MTurkParams)):
    logger.info(f"GET request on {PREFIX}/{rs_id}")
    sample = rh.load_ranking_sample(rs_id)
    if sample is not None:
        sample.add_mt_params(mt)

    return sample
