from typing import Union, Optional, List

from fastapi import APIRouter, Depends
from loguru import logger

from backend import LikertStudyCoordinator
from backend.auth import JWTBearer
from backend.db import RedisHandler
from models import RankingSample, MTurkParams
from models.likert_sample import LikertSample

PREFIX = "/likert_sample"
TAG = ["likert_sample"]
router = APIRouter()

rh = RedisHandler()
coord = LikertStudyCoordinator()


@logger.catch(reraise=True)
@router.get("/next", tags=TAG,
            response_model=Union[LikertSample, int],
            description="Returns the next LikertSample or the shortest waiting time in seconds until the next sample "
                        "is ready.")
async def get_next_likert_sample():
    logger.info(f"GET request on {PREFIX}/next")
    return coord.next()


@logger.catch(reraise=True)
@router.get("/list", tags=TAG,
            response_model=List[LikertSample],
            description="Returns all LikertSamples",
            dependencies=[Depends(JWTBearer())])
async def list_likert_samples(num: int = 100):
    logger.info(f"GET request on {PREFIX}/list")
    return rh.list_likert_samples(num)


@logger.catch(reraise=True)
@router.get("/{ls_id}", tags=TAG,
            response_model=RankingSample,
            description="Returns the RankingSample with the specified ID")
async def load_sample(ls_id: str, mt: Optional[MTurkParams] = Depends(MTurkParams)):
    logger.info(f"GET request on {PREFIX}/{ls_id}")
    sample = rh.load_likert_sample(ls_id)
    if sample is not None:
        sample.add_mt_params(mt)

    return sample
