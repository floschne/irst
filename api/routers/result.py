from fastapi import APIRouter
from loguru import logger
from starlette.responses import JSONResponse

from backend.db import RedisHandler
from models import EvalResult

PREFIX = "/result"
TAG = ["result"]

router = APIRouter()

redis = RedisHandler()


@router.get("/{result_id}", tags=TAG,
            response_model=EvalResult,
            description="Returns the EvalResult with the specified ID")
async def load_sample(result_id: str):
    logger.info(f"GET request on {PREFIX}/{result_id}")
    return redis.load_result(result_id)


@router.put("/store", tags=TAG,
            description="Stores the EvalSample")
async def store_result(result: EvalResult):
    logger.info(f"GET request on {PREFIX}/store")
    id = redis.store_result(result)
    return JSONResponse(content=id)
