import uvicorn
from fastapi import FastAPI
from loguru import logger
from omegaconf import OmegaConf

from backend import StudyCoordinator, ImageServer
from backend.auth import AuthHandler
from backend.db import RedisHandler
from routers import general, eval_sample, result, image, study, mranking, user

# create the main api
app = FastAPI(title="User Study API",
              description="Simple API that powers my Master Thesis' user study.",
              version="beta")


@logger.catch(reraise=True)
@app.on_event("startup")
def startup_event():
    try:
        conf = OmegaConf.load('config/config.yml')

        # setup logger
        logger.add('logs/{time}.log', rotation=f"{conf.logging.rotation} MB", level=conf.logging.level)

        # init redis
        RedisHandler()

        # init auth handler
        auth = AuthHandler()
        auth.register_admin()

        # init image server
        img_srv = ImageServer()
        img_srv.init_image_data()

        # init study
        coord = StudyCoordinator()
        coord.init_study()

    except Exception as e:
        msg = f"Error while starting the API! Exception: {str(e)}"
        logger.error(msg)
        raise SystemExit(msg)


@logger.catch(reraise=True)
@app.on_event("shutdown")
def shutdown_event():
    RedisHandler().shutdown()
    StudyCoordinator().shutdown()


# include the routers
app.include_router(general.router)
app.include_router(eval_sample.router, prefix=eval_sample.PREFIX)
app.include_router(result.router, prefix=result.PREFIX)
app.include_router(image.router, prefix=image.PREFIX)
app.include_router(study.router, prefix=study.PREFIX)
app.include_router(mranking.router, prefix=mranking.PREFIX)
app.include_router(user.router, prefix=user.PREFIX)

# entry point for main.py
if __name__ == "__main__":
    # load config
    conf = OmegaConf.load('config/config.yml')

    # start the api via uvicorn
    assert conf.port is not None and isinstance(conf.port, int), "The port has to be an integer! E.g. 8081"
    uvicorn.run(app, host="0.0.0.0", port=conf.port, debug=True, lifespan="on")
