from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from backend.auth import AuthHandler
from backend.auth import JWTBearer
from models.user import User

PREFIX = "/user"
TAG = ["user"]

router = APIRouter()


@logger.catch(reraise=True)
@router.post("/authenticate", tags=TAG,
             description="Authenticates a user and returns a JWT.")
async def authenticate(user: User):
    logger.info(f"POST request on {PREFIX}/authenticate")
    token = AuthHandler().authenticate(user)
    if token is None:
        raise HTTPException(status_code=403, detail="Invalid user information provided!")
    return token


@logger.catch(reraise=True)
@router.post("/register", tags=TAG,
             description="Registers a new users")
async def register(user: User):
    logger.info(f"POST request on {PREFIX}/register")
    return AuthHandler().register(user)


@logger.catch(reraise=True)
@router.post("/renew_jwt", tags=TAG,
             description="Renews the JWT for of the given user",
             dependencies=[Depends(JWTBearer(admin_only=False))])
async def renew_jwt(user: User):
    logger.info(f"POST request on {PREFIX}/renew_jwt")
    return AuthHandler().renew_jwt(user)
