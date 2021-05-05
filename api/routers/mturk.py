from typing import Optional, List

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
            description="Creates a HIT for the RankingSample with the given ES ID",
            dependencies=[Depends(JWTBearer())])
async def create_hit(rs_id: str, creds: Optional[AWSCreds], sandbox: Optional[bool] = True):
    logger.info(f"PUT request on {PREFIX}/hit/create")
    rs = rh.load_ranking_sample(rs_id=rs_id)
    if rs is not None:
        if creds is not None:
            mturk.create_new_client(sandbox, creds.access_key, creds.secret)
        return mturk.create_hit_from_rs(rs)
    return False


@logger.catch(reraise=True)
@router.put("/hits/create", tags=TAG,
            description="Creates a HIT for every RankingSample of the Study (current run)",
            dependencies=[Depends(JWTBearer())])
async def create_hits(creds: Optional[AWSCreds], sandbox: Optional[bool] = True):
    logger.info(f"PUT request on {PREFIX}/hits/create")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    rs = rh.list_ranking_samples()
    return mturk.create_hits_from_rs(rs)


@logger.catch(reraise=True)
@router.delete("/hit/delete", tags=TAG,
               description="Deletes the HIT with the given ID",
               dependencies=[Depends(JWTBearer())])
async def delete_hit(hit_id: str, creds: Optional[AWSCreds], sandbox: Optional[bool] = True):
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
@router.get("/hit/info/rs/{rs_id}", tags=TAG,
            description="Returns the HIT Info associated with the RankingSample with the given ID",
            dependencies=[Depends(JWTBearer())])
async def hit_info(rs_id: str):
    logger.info(f"GET request on {PREFIX}/hit/info/rs/{rs_id}")
    rs = rh.load_ranking_sample(rs_id=rs_id)
    if rs is not None:
        return mturk.get_hit_info_via_rs(rs)
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
@router.post("/assignments/approve/", tags=TAG,
             description="Approves the Assignments with the given IDs",
             dependencies=[Depends(JWTBearer())])
async def approve_assignments(assignment_ids: List[str],
                              feedback: Optional[str] = "",
                              creds: Optional[AWSCreds] = None,
                              sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/assignments/approve/")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.approve_assignments(assignment_ids=assignment_ids, feedback=feedback)


@logger.catch(reraise=True)
@router.post("/assignments/approve/{ass_id}", tags=TAG,
             description="Approves the Assignment with the given ID",
             dependencies=[Depends(JWTBearer())])
async def approve_assignment(assignment_id: str,
                             feedback: Optional[str] = "",
                             creds: Optional[AWSCreds] = None,
                             sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/assignments/approve/{assignment_id}")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.approve_assignment(assignment_id=assignment_id, feedback=feedback)


@logger.catch(reraise=True)
@router.post("/assignments/{hit_id}", tags=TAG,
             description="Returns all Assignments of the HIT with the given ID",
             dependencies=[Depends(JWTBearer())])
async def list_assignments_for_hit(hit_id: str, creds: Optional[AWSCreds], sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/assignments/{hit_id}")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.list_assignments_for_hit(hit_id)


@logger.catch(reraise=True)
@router.post("/qualification/associate_worker", tags=TAG,
             description="Associates the Qualification with the given ID with the specified Worker",
             dependencies=[Depends(JWTBearer())])
async def associate_qualification_with_worker(worker_id: str,
                                              qualification_type_id: str,
                                              integer_value: Optional[int] = 1312,
                                              creds: Optional[AWSCreds] = None,
                                              sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/qualification/associate_worker/")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.associate_qualification_with_worker(worker_id=worker_id,
                                                     qualification_type_id=qualification_type_id,
                                                     integer_value=integer_value)


@logger.catch(reraise=True)
@router.post("/qualification/associate_workers", tags=TAG,
             description="Associates the Qualification with the given ID with the specified Worker",
             dependencies=[Depends(JWTBearer())])
async def associate_qualification_with_workers(worker_ids: List[str],
                                               qualification_type_id: str,
                                               integer_value: Optional[int] = 1312,
                                               creds: Optional[AWSCreds] = None,
                                               sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/qualification/associate_workers/")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.associate_qualification_with_workers(worker_ids=worker_ids,
                                                      qualification_type_id=qualification_type_id,
                                                      integer_value=integer_value)


@logger.catch(reraise=True)
@router.post("/qualification/disassociate_worker", tags=TAG,
             description="Disassociates the Qualification with the given ID with the specified Worker",
             dependencies=[Depends(JWTBearer())])
async def disassociate_qualification_with_worker(worker_id: str,
                                                 qualification_type_id: str,
                                                 reason: Optional[str] = "No Reason",
                                                 creds: Optional[AWSCreds] = None,
                                                 sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/qualification/disassociate_worker/")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.disassociate_qualification_with_worker(worker_id=worker_id,
                                                        qualification_type_id=qualification_type_id,
                                                        reason=reason)


@logger.catch(reraise=True)
@router.post("/qualification/disassociate_workers", tags=TAG,
             description="Disassociates the Qualification with the given ID with the specified Worker",
             dependencies=[Depends(JWTBearer())])
async def disassociate_qualification_with_workers(worker_ids: List[str],
                                                  qualification_type_id: str,
                                                  reason: Optional[str] = "No Reason",
                                                  creds: Optional[AWSCreds] = None,
                                                  sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/qualification/disassociate_workers/")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.disassociate_qualification_with_workers(worker_ids=worker_ids,
                                                         qualification_type_id=qualification_type_id,
                                                         reason=reason)


@logger.catch(reraise=True)
@router.post("/workers/notify", tags=TAG,
             description="Sends an email to one or more Workers specified with the Worker IDs",
             dependencies=[Depends(JWTBearer())])
async def notify_workers(subject: str,
                         message_text: str,
                         worker_ids: List[str],
                         creds: Optional[AWSCreds] = None,
                         sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/workers/notify/")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.notify_workers(subject=subject,
                                message_text=message_text,
                                worker_ids=worker_ids)


@logger.catch(reraise=True)
@router.post("/account/balance", tags=TAG,
             description="Get the account balance",
             dependencies=[Depends(JWTBearer())])
async def get_account_balance(creds: Optional[AWSCreds] = None,
                              sandbox: Optional[bool] = True):
    logger.info(f"GET request on {PREFIX}/account/balance/")
    if creds is not None:
        mturk.create_new_client(sandbox, creds.access_key, creds.secret)
    return mturk.get_account_balance()
