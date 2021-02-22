import uvicorn
from fastapi import FastAPI
from loguru import logger
from omegaconf import OmegaConf

from routers import general


# entry point for uvicorn CLI (used e.g. via Docker)
def build_api():
    # setup logger
    logger.add('logs/{time}.log', rotation="500 MB")

    # create the main api
    api = FastAPI(title="User Study API",
                  description="Simple API that powers my Master Thesis' user study.",
                  version="beta")

    # include the routers
    api.include_router(general.router)

    return api


# entry point for main.py
def main(conf):
    # create the main api
    api = build_api()

    # start the api via uvicorn
    assert conf.port is not None and isinstance(conf.port, int), "The port has to be an integer! E.g. 8081"
    uvicorn.run(api, host="0.0.0.0", port=conf.port, debug=True)


if __name__ == "__main__":
    # load config
    conf = OmegaConf.load('config/config.yml')
    main(conf)
