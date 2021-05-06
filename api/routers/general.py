from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from loguru import logger

router = APIRouter()


@logger.catch(reraise=True)
@router.get("/heartbeat", tags=["general"], description="Return True if the API is alive and running")
async def heartbeat():
    logger.info("GET request on /heartbeat")
    return True  # TODO JSONResponse(content=StudyCoordinator().initialization_is_done())


@logger.catch(reraise=True)
@router.get("/", tags=["general"], description="Redirection to /docs")
async def redirect_to_docs():
    logger.info("GET request on / -> redirecting to /docs")
    return RedirectResponse("/docs")
