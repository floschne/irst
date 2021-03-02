from typing import List

from fastapi import APIRouter
from loguru import logger

from backend import ImageServer

PREFIX = "/image"
TAG = ["image"]

router = APIRouter()


@router.get("/url/{img_id}", tags=TAG,
            description="Returns the URL of the image with the specified ID")
async def get_url(img_id: str):
    logger.info(f"GET request on {PREFIX}/url/{img_id}")
    return ImageServer().get_img_url(img_id)


@router.post("/urls", tags=TAG,
             response_model=List[str],
             description="Returns the URL of the image with the specified ID")
async def get_urls(img_ids: List[str]):
    logger.info(f"GET request on {PREFIX}/urls")
    return ImageServer().get_img_urls(img_ids)
