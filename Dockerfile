FROM python:3.8.2-alpine3.11 as builder
MAINTAINER Paritosh Gupta <pg@totalitycorp.com>

RUN apk add --update --no-cache \
    gcc \
    linux-headers \
    make \
    musl-dev \
    python3-dev \
    zlib-dev \
    libjpeg-turbo-dev \
    g++

ENV GRPC_PYTHON_VERSION 1.15.0

RUN pip install virtualenv
# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
RUN virtualenv /env

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV -p python3.8.2 /env
ENV PATH /env/bin:$PATH

COPY requirements.txt /app/
RUN pip install --requirement /app/requirements.txt
# COPY . /app/
# EXPOSE 50051
# ENTRYPOINT []
# CMD ["python", "/app/server.py"]


### FINAL DOCKER
FROM python:3.8.2-alpine3.11
MAINTAINER Paritosh Gupta <pg@totalitycorp.com>

RUN apk --no-cache --update add libstdc++ \
    zlib-dev \
    libjpeg-turbo-dev \
    && rm -Rf /var/cache/apk/*

RUN \
  pip install --upgrade pip && \
  pip install --upgrade virtualenv 


COPY --from=builder /env /env
ENV PATH /env/bin:$PATH

COPY . /app/

RUN ls  /env
RUN ls  /app

EXPOSE 50051
CMD ["python", "/app/server.py"]

#docker run -d --name vision  --env-file=.env -p 50051:50051 asia.gcr.io/chrome-weft-229408/vision:v1