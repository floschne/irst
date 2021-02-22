import uvicorn
from fastapi import FastAPI
from loguru import logger
from omegaconf import OmegaConf

from backend.db import RedisHandler
from routers import general, sample

# setup logger
logger.add('logs/{time}.log', rotation="500 MB")

# create the main api
api = FastAPI(title="User Study API",
              description="Simple API that powers my Master Thesis' user study.",
              version="beta")


@api.on_event("startup")
def startup_event():
    try:
        # instantiate singletons
        RedisHandler()
    except Exception as e:
        msg = f"Error while starting the API! Exception: {str(e)}"
        logger.error(msg)
        raise SystemExit(msg)


@api.on_event("shutdown")
def shutdown_event():
    RedisHandler().__close()


# include the routers
api.include_router(general.router)
api.include_router(sample.router, prefix=sample.PREFIX)

# entry point for main.py
if __name__ == "__main__":
    # load config
    conf = OmegaConf.load('config/config.yml')

    # start the api via uvicorn
    assert conf.port is not None and isinstance(conf.port, int), "The port has to be an integer! E.g. 8081"
    uvicorn.run(api, host="0.0.0.0", port=conf.port, debug=True)
