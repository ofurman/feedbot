FROM python:3.7-alpine

LABEL Name=feedbot Version=0.0.1
EXPOSE 5001

RUN apk update && apk add libpq
RUN apk add --no-cache build-base
RUN apk add --virtual .build-deps gcc python-dev musl-dev postgresql-dev

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt /usr/src/app

RUN python3 -m pip install -r requirements.txt

RUN apk del .build-deps

ADD . /usr/src/app

CMD ["python3", "/usr/src/app/main.py"]