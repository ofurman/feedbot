FROM python:3.7-alpine

LABEL Name=feedbot Version=0.0.1
EXPOSE 5001

RUN apk update && apk upgrade -y
RUN apk add --no-cache build-base

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ADD ./bot /usr/src/app

RUN python3 -m pip install -r requirements.txt
CMD ["python3", "/usr/src/app/main.py"]