from fastapi import APIRouter
from loguru import logger
from starlette.responses import JSONResponse

from backend.db import RedisHandler
from models import EvalSample

PREFIX = "/sample"
TAG = ["sample"]
router = APIRouter()

redis = RedisHandler()


@router.get("/random", tags=TAG,
            response_model=EvalSample,
            description="Returns a random EvalSample")
async def random():
    logger.info(f"GET request on {PREFIX}/random")
    return redis.random_sample()


@router.get("/{sample_id}", tags=TAG,
            response_model=EvalSample,
            description="Returns the EvalSample with the specified ID")
async def load_sample(sample_id: str):
    logger.info(f"GET request on {PREFIX}/{sample_id}")
    return redis.load_sample(sample_id)


@router.put("/store", tags=TAG,
            description="Stores the EvalSample")
async def store_sample(sample: EvalSample):
    logger.info(f"GET request on {PREFIX}/store")
    id = redis.store_sample(sample)
    return JSONResponse(content=id)
