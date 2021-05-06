import uvicorn
from fastapi import FastAPI
from loguru import logger

from backend import RankingStudyCoordinator, LikertStudyCoordinator, ImageServer
from backend.auth import AuthHandler
from backend.db import RedisHandler
from backend.mturk import MTurkHandler
from config import conf
from routers import general, ranking_sample, ranking_result, likert_sample, likert_result, image, study, mranking, user, mturk, feedback

# create the main api
app = FastAPI(title="User Study API",
              description="Simple API that powers my Master Thesis' user study.",
              version="beta")


@logger.catch(reraise=True)
@app.on_event("startup")
def startup_event():
    try:
        # setup logger
        logger.add('logs/{time}.log', rotation=f"{conf.logging.rotation} MB", level=conf.logging.level)

        # init redis
        rh = RedisHandler()
        # flush all redis dbs if set
        if conf.study_initialization.flush:
            rh.flush()

        # init auth handler
        auth = AuthHandler()
        auth.register_admin()

        # init image server
        img_srv = ImageServer()
        img_srv.init_image_data()

        # init study coordinators
        ranking_coord = RankingStudyCoordinator()
        ranking_coord.init_study()
        likert_coord = LikertStudyCoordinator()
        likert_coord.init_study()

        # init mturk
        mt = MTurkHandler()
        mt.init_hit_types()

    except Exception as e:
        msg = f"Error while starting the API! Exception: {str(e)}"
        logger.error(msg)
        raise SystemExit(msg)


@logger.catch(reraise=True)
@app.on_event("shutdown")
def shutdown_event():
    RedisHandler().shutdown()
    RankingStudyCoordinator().shutdown()
    LikertStudyCoordinator().shutdown()
    AuthHandler().shutdown()


# include the routers
app.include_router(general.router)
app.include_router(ranking_sample.router, prefix=ranking_sample.PREFIX)
app.include_router(ranking_result.router, prefix=ranking_result.PREFIX)
app.include_router(likert_sample.router, prefix=likert_sample.PREFIX)
app.include_router(likert_result.router, prefix=likert_result.PREFIX)
app.include_router(image.router, prefix=image.PREFIX)
app.include_router(study.router, prefix=study.PREFIX)
app.include_router(mranking.router, prefix=mranking.PREFIX)
app.include_router(user.router, prefix=user.PREFIX)
app.include_router(mturk.router, prefix=mturk.PREFIX)
app.include_router(feedback.router, prefix=feedback.PREFIX)

# entry point for main.py
if __name__ == "__main__":
    # start the api via uvicorn
    assert conf.port is not None and isinstance(conf.port, int), "The port has to be an integer! E.g. 8081"
    uvicorn.run(app, host="0.0.0.0", port=conf.port, debug=True, lifespan="on")
