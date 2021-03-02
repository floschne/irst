from typing import Union

from fastapi import APIRouter
from loguru import logger

from backend import StudyCoordinator
from backend.db import RedisHandler
from models import EvalSample

PREFIX = "/sample"
TAG = ["sample"]
router = APIRouter()

redis = RedisHandler()
coordinator = StudyCoordinator()


@router.get("/next", tags=TAG,
            response_model=Union[EvalSample, int],
            description="Returns the next EvalSample or the shortest waiting time until the next sample is ready.")
async def get_next():
    logger.info(f"GET request on {PREFIX}/next")
    return coordinator.next()


@router.get("/{sample_id}", tags=TAG,
            response_model=EvalSample,
            description="Returns the EvalSample with the specified ID")
async def load_sample(sample_id: str):
    logger.info(f"GET request on {PREFIX}/{sample_id}")
    return redis.load_eval_sample(sample_id)
