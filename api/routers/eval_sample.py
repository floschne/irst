from typing import Union, Optional, List

from fastapi import APIRouter, Depends
from loguru import logger

from backend import StudyCoordinator
from backend.auth import JWTBearer
from backend.db import RedisHandler
from models import EvalSample, MTurkParams

PREFIX = "/sample"
TAG = ["sample"]
router = APIRouter()

rh = RedisHandler()
coord = StudyCoordinator()


@logger.catch(reraise=True)
@router.get("/next", tags=TAG,
            response_model=Union[EvalSample, int],
            description="Returns the next EvalSample or the shortest waiting time until the next sample is ready.")
async def get_next_sample():
    logger.info(f"GET request on {PREFIX}/next")
    return coord.next()


@logger.catch(reraise=True)
@router.get("/list", tags=TAG,
            response_model=List[EvalSample],
            description="Returns all EvalSamples",
            dependencies=[Depends(JWTBearer())])
async def list_samples(num: int = 100):
    logger.info(f"GET request on {PREFIX}/list")
    return rh.list_eval_samples(num)


@logger.catch(reraise=True)
@router.get("/{sample_id}", tags=TAG,
            response_model=EvalSample,
            description="Returns the EvalSample with the specified ID")
async def load_sample(sample_id: str, mt: Optional[MTurkParams] = Depends(MTurkParams)):
    logger.info(f"GET request on {PREFIX}/{sample_id}")
    sample = rh.load_eval_sample(sample_id)
    if sample is not None:
        sample.add_mt_params(mt)

    return sample
