from typing import Union, Optional, List

from fastapi import APIRouter, Depends
from loguru import logger

from backend.auth import JWTBearer
from backend.db import RedisHandler
from backend.study import RatingStudyCoordinator
from models import RatingSample, MTurkParams

PREFIX = "/rating_sample"
TAG = ["rating_sample"]
router = APIRouter()

rh = RedisHandler()


@logger.catch(reraise=True)
@router.get("/next", tags=TAG,
            response_model=Union[RatingSample, int],
            description="Returns the next RatingSample or the shortest waiting time in seconds until the next sample "
                        "is ready.")
async def get_next_rating_sample():
    logger.info(f"GET request on {PREFIX}/next")
    coord = RatingStudyCoordinator()
    return coord.next()


@logger.catch(reraise=True)
@router.get("/list", tags=TAG,
            response_model=List[RatingSample],
            description="Returns all RatingSamples",
            dependencies=[Depends(JWTBearer())])
async def list_rating_samples(num: int = 100):
    logger.info(f"GET request on {PREFIX}/list")
    return rh.list_rating_samples(num)


@logger.catch(reraise=True)
@router.get("/{rs_id}", tags=TAG,
            response_model=RatingSample,
            description="Returns the RatingSample with the specified ID")
async def load_sample(rs_id: str, mt: Optional[MTurkParams] = Depends(MTurkParams)):
    logger.info(f"GET request on {PREFIX}/{rs_id}")
    sample = rh.load_rating_sample(rs_id)
    if sample is not None:
        sample.add_mt_params(mt)

    return sample
