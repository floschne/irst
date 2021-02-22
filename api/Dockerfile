FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
MAINTAINER Florian Schneider "florian.schneider.1992@gmx.de"

COPY . /app/
RUN pip install -r /app/requirements.txt

ENV MAX_WORKERS="16"
ENV LOG_LEVEL="debug"
