from fastapi import APIRouter
from loguru import logger

from backend import ImageServer

PREFIX = "/image"
TAG = ["image"]

router = APIRouter()

@router.get("/url/{img_id}", tags=TAG,
            description="Returns the URL of the image with the specified ID")
async def url(img_id: str):
    logger.info(f"GET request on {PREFIX}/{img_id}")
    return ImageServer().get_img_url(img_id)
