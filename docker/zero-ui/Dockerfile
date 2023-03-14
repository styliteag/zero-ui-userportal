FROM node:lts-alpine as build-stage

ENV INLINE_RUNTIME_CHUNK=false
ENV GENERATE_SOURCEMAP=false
RUN apk add --no-cache tzdata
ENV TZ Europe/Berlin 


WORKDIR /app/frontend
COPY ./frontend/package*.json /app/frontend
RUN yarn install --network-timeout 5000000

COPY ./frontend /app/frontend
RUN yarn build

#### Python Backend
FROM alpine:latest

RUN apk add --update python3-dev && ln -sf python3 /usr/bin/python
RUN apk add libffi-dev
RUN apk add gcc
RUN apk add musl-dev
RUN apk add --no-cache tzdata

ENV TZ Europe/Berlin 

COPY ./backend-py/requirements.txt /app/requirements.txt

RUN python3 -m ensurepip
RUN pip3 install --upgrade pip setuptools
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./backend-py /app

COPY --from=build-stage /app/frontend/dist /app/app/
ENV FLASK_APP=main.py
EXPOSE 80

WORKDIR /app
CMD ["python", "main.py"]