from fastapi import APIRouter
from loguru import logger
from starlette.responses import JSONResponse

from backend.db import RedisHandler
from models import EvalResult

PREFIX = "/result"
TAG = ["result"]

router = APIRouter()

redis = RedisHandler()


@logger.catch(reraise=True)
@router.get("/{result_id}", tags=TAG,
            response_model=EvalResult,
            description="Returns the EvalResult with the specified ID")
async def load(result_id: str):
    logger.info(f"GET request on {PREFIX}/{result_id}")
    return redis.load_result(result_id)


@logger.catch(reraise=True)
@router.put("/submit", tags=TAG,
            description="Submit an EvalResult")
async def submit(result: EvalResult):
    logger.info(f"GET request on {PREFIX}/submit")
    return JSONResponse(content=redis.store_result(result))
