from typing import List, Optional

from fastapi import APIRouter, Depends
from loguru import logger

from backend.auth import JWTBearer
from backend.db import RedisHandler
from models.feedback import Feedback

PREFIX = "/feedback"
TAG = ["feedback"]

router = APIRouter()
rh = RedisHandler()


@logger.catch(reraise=True)
@router.put("/submit", tags=TAG,
            description="Stores a Feedback for a given Sample,")
async def submit_feedback(feedback: Feedback):
    logger.info(f"PUT request on {PREFIX}/submit")
    return rh.store_feedback(feedback=feedback)


@logger.catch(reraise=True)
@router.get("/load/{fb_id}", tags=TAG,
            response_model=Optional[Feedback],
            description="Loads the Feedbacks with the given ID",
            dependencies=[Depends(JWTBearer())])
async def load_feedback(fb_id: str):
    logger.info(f"GET request on {PREFIX}/load/{fb_id}")
    return rh.load_feedback(fb_id=fb_id)


@logger.catch(reraise=True)
@router.get("/list/rs/{rs_id}", tags=TAG,
            description="Lists all Feedbacks of the Sample with the given ID",
            dependencies=[Depends(JWTBearer())],
            response_model=List[Feedback])
async def list_feedbacks_for_ranking_sample(rs_id: str):
    logger.info(f"GET request on {PREFIX}/list/rs/{rs_id}")
    return rh.list_feedbacks_of_sample(sample_id=rs_id)


@logger.catch(reraise=True)
@router.get("/list", tags=TAG,
            description="Lists all Feedbacks",
            dependencies=[Depends(JWTBearer())],
            response_model=List[Feedback])
async def list_all_feedbacks():
    logger.info(f"GET request on {PREFIX}/list")
    return rh.list_all_feedbacks()
