from typing import List

from fastapi import APIRouter
from loguru import logger

from backend import ImageServer

PREFIX = "/image"
TAG = ["image"]

router = APIRouter()


@logger.catch(reraise=True)
@router.get("/url/{img_id}", tags=TAG,
            description="Returns the URL of the image with the specified ID")
async def get_url(img_id: str):
    logger.info(f"GET request on {PREFIX}/url/{img_id}")
    return ImageServer().get_img_url(img_id)


@logger.catch(reraise=True)
@router.post("/urls", tags=TAG,
             response_model=List[str],
             description="Returns the URL of the image with the specified ID")
async def get_urls(img_ids: List[str]):
    logger.info(f"GET request on {PREFIX}/urls")
    return ImageServer().get_img_urls(img_ids)


@logger.catch(reraise=True)
@router.post("/ids", tags=TAG,
             response_model=List[str],
             description="Returns the IDs of the Image URLs")
async def get_urls(img_urls: List[str]):
    logger.info(f"GET request on {PREFIX}/ids")
    return ImageServer().get_img_ids(img_urls)