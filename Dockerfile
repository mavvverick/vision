FROM python:3.8.2-alpine3.11
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
COPY . /app/

EXPOSE 50051
ENTRYPOINT []

CMD ["python", "/app/server.py"]