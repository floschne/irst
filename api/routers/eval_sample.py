from typing import Union, Optional

from fastapi import APIRouter, Depends
from loguru import logger

from backend import StudyCoordinator
from backend.db import RedisHandler
from models import EvalSample, MTurkParams

PREFIX = "/sample"
TAG = ["sample"]
router = APIRouter()

redis = RedisHandler()
coordinator = StudyCoordinator()


@logger.catch(reraise=True)
@router.get("/next", tags=TAG,
            response_model=Union[EvalSample, int],
            description="Returns the next EvalSample or the shortest waiting time until the next sample is ready.")
async def get_next_sample():
    logger.info(f"GET request on {PREFIX}/next")
    return coordinator.next()


@logger.catch(reraise=True)
@router.get("/{sample_id}", tags=TAG,
            response_model=EvalSample,
            description="Returns the EvalSample with the specified ID")
async def load_sample(sample_id: str, mt: Optional[MTurkParams] = Depends(MTurkParams)):
    logger.info(f"GET request on {PREFIX}/{sample_id}")
    sample = redis.load_eval_sample(sample_id)
    sample.add_mt_params(mt)

    return sample
