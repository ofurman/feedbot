FROM python:3.7-alpine

LABEL Name=manager Version=0.0.1
EXPOSE 5001

RUN apk update && apk upgrade
RUN apk add --no-cache build-base

RUN mkdir /usr/src/manager
WORKDIR /usr/src/manager
COPY ./requirements.txt /usr/src/manager

RUN python3 -m pip install -r requirements.txt


ADD . /usr/src/manager


CMD ["python3", "/usr/src/manager/main.py"]