from fastapi import APIRouter, Depends
from loguru import logger
from starlette.responses import JSONResponse

from backend import StudyCoordinator
from backend.auth import JWTBearer
from backend.db import RedisHandler
from models import EvalResult

PREFIX = "/result"
TAG = ["result"]

router = APIRouter()

redis = RedisHandler()
sc = StudyCoordinator()


@logger.catch(reraise=True)
@router.get("/{result_id}", tags=TAG,
            response_model=EvalResult,
            description="Returns the EvalResult with the specified ID",
            dependencies=[Depends(JWTBearer())])
async def load(result_id: str):
    logger.info(f"GET request on {PREFIX}/{result_id}")
    return redis.load_result(result_id)


@logger.catch(reraise=True)
@router.put("/submit", tags=TAG,
            description="Submit an EvalResult")
async def submit(result: EvalResult):
    logger.info(f"GET request on {PREFIX}/submit")
    return JSONResponse(content=sc.submit(result))
