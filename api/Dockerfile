FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
MAINTAINER Florian Schneider "florian.schneider.1992@gmx.de"

ADD requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY . /app/

ENV MAX_WORKERS="4"
ENV LOG_LEVEL="debug"
