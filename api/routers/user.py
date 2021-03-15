from fastapi import APIRouter, HTTPException
from loguru import logger

from backend.auth import AuthHandler
from models.user import User

PREFIX = "/user"
TAG = ["user"]

router = APIRouter()


@logger.catch(reraise=True)
@router.post("/authenticate", tags=TAG,
             description="Returns the current progress of the Study")
async def authenticate(user: User):
    logger.info(f"GET request on {PREFIX}/login")
    token = AuthHandler().authenticate(user)
    if token is None:
        raise HTTPException(status_code=403, detail="Invalid user information provided!")
    return token
