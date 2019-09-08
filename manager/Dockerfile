FROM python:3.7-alpine

LABEL Name=manager Version=0.0.1
EXPOSE 5001

RUN apk update && apk add libpq
RUN apk add --no-cache build-base
RUN apk add --virtual .build-deps gcc python-dev musl-dev postgresql-dev

RUN mkdir /usr/src/manager
WORKDIR /usr/src/manager
COPY ./requirements.txt /usr/src/manager

RUN python3 -m pip install -r requirements.txt

RUN apk del .build-deps

ADD . /usr/src/manager

CMD ["python3", "/usr/src/manager/main.py"]