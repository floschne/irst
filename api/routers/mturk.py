from typing import Optional

from fastapi import APIRouter, Depends
from loguru import logger

from backend.auth import JWTBearer
from backend.db import RedisHandler
from backend.mturk import MTurkHandler
from models import AWSCreds

PREFIX = "/mturk"
TAG = ["mturk"]

router = APIRouter()

mturk = MTurkHandler()
rh = RedisHandler()


@logger.catch(reraise=True)
@router.put("/hit/create", tags=TAG,
            description="Creates a HIT for the EvalSample with the given ES ID",
            dependencies=[Depends(JWTBearer())])
async def create_hit(es_id: str, creds: Optional[AWSCreds], sandbox: Optional[bool] = True):
    logger.info(f"PUT request on {PREFIX}/hit/create")
    es = rh.load_eval_sample(sample_id=es_id)
    if es is not None:
        if creds is not None:
            mturk.create_new_client(sandbox, creds.access_key, creds.secret)
        return mturk.create_hit_from_es(es)
    return False


@logger.catch(reraise=True)
@router.put("/hits/create", tags=TAG,
            description="Creates a HIT for every EvalSample of the Study (current run)",
            dependencies=[Depends(JWTBearer())])
async def create_hits(creds: Optional[AWSCreds], sandbox: Optional[bool] = True):
    logger.info(f"PUT request on {PREFIX}/hits/create")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    es = rh.list_eval_samples()
    return mturk.create_hits_from_es(es)


@logger.catch(reraise=True)
@router.delete("/hit/delete", tags=TAG,
               description="Deletes the HIT with the given ID",
               dependencies=[Depends(JWTBearer())])
async def delete_hit(hit_id: str,creds: Optional[AWSCreds],  sandbox: Optional[bool] = True):
    logger.info(f"DELETE request on {PREFIX}/hit/delete")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.delete_hit(hit_id)


@logger.catch(reraise=True)
@router.delete("/hits/delete", tags=TAG,
               description="Deletes all HITs associated with this Study",
               dependencies=[Depends(JWTBearer())])
async def delete_all_hit(creds: Optional[AWSCreds], sandbox: Optional[bool] = True):
    logger.info(f"DELETE request on {PREFIX}/hits/delete")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.delete_all_hits()


@logger.catch(reraise=True)
@router.post("/hits/ids", tags=TAG,
            description="Returns all HIT IDs",
            dependencies=[Depends(JWTBearer())])
async def list_hit_ids(creds: Optional[AWSCreds], sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/hits/ids")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.list_hit_ids()


@logger.catch(reraise=True)
@router.post("/hits/list", tags=TAG,
            description="Returns all HITs",
            dependencies=[Depends(JWTBearer())])
async def list_hit(creds: Optional[AWSCreds], sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/hits/list")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.list_hits()


@logger.catch(reraise=True)
@router.get("/hit/info/{hit_id}", tags=TAG,
            description="Returns the Info of the HIT with the given ID",
            dependencies=[Depends(JWTBearer())])
async def hit_info(hit_id: str):
    logger.info(f"GET request on {PREFIX}/hit/info/{hit_id}")
    return mturk.get_hit_info(hit_id)


@logger.catch(reraise=True)
@router.get("/hit/info/es/{es_id}", tags=TAG,
            description="Returns the HIT Info associated with the EvalSample with the given ID",
            dependencies=[Depends(JWTBearer())])
async def hit_info(es_id: str):
    logger.info(f"GET request on {PREFIX}/hit/info/es/{es_id}")
    es = rh.load_eval_sample(sample_id=es_id)
    if es is not None:
        return mturk.get_hit_info_via_es(es)
    return None


@logger.catch(reraise=True)
@router.post("/assignments/reviewable", tags=TAG,
            description="Returns the all reviewable Assignments associated with this Study",
            dependencies=[Depends(JWTBearer())])
async def list_reviewable_assignments(creds: Optional[AWSCreds], sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/assignments/reviewable")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.list_reviewable_assignments()


@logger.catch(reraise=True)
@router.post("/assignments/{hit_id}", tags=TAG,
            description="Returns all Assignments of the HIT with the given ID",
            dependencies=[Depends(JWTBearer())])
async def list_assignments_for_hit(hit_id: str, creds: Optional[AWSCreds], sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/assignments/{hit_id}")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.list_assignments_for_hit(hit_id)
