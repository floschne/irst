import time
from datetime import datetime

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from loguru import logger

from .auth_handler import AuthHandler


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, admin_only: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.admin_only = admin_only

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authorization scheme.")
            else:
                self.verify_jwt(credentials.credentials)
                return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt: str) -> bool:
        payload = AuthHandler().decode_jwt(jwt)
        if payload is None:
            logger.warning("Invalid Token!")
            raise HTTPException(status_code=403, detail="Invalid token!")
        elif self.admin_only:
            if not AuthHandler().is_admin(payload['user_id']):
                logger.warning(f"Unauthorized request from non-admin User {payload['user_id']}!")
                raise HTTPException(status_code=403, detail="Unauthorized request. Only Administrators are allowed!")
        elif payload['ttl'] <= time.time():
            logger.warning(f"JWT Expired at {datetime.fromtimestamp(payload['ttl'])}!")
            raise HTTPException(status_code=403, detail=f"Expired token! This token expired at {payload['ttl']}")
        return True
