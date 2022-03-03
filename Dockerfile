#@IgnoreInspection BashAddShebang
############################################################
# DKGeneralPurposeContainer
# Dockerfile to build Analytic Container Template
############################################################

FROM ubuntu:20.04

MAINTAINER Carlos E. Descalzi <carlos@datakitchen.io>

ENV LC_CTYPE=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends tzdata

# Install basic applications
RUN apt-get install --yes \
    python3 \
    python3-pip

# Set the default directory where CMD will execute
WORKDIR /dk

# Copy gpc stuff
COPY ./icon.svg                         /dk/icon.svg

COPY ./src /dk/lib

ENV PYTHONPATH=/dk/lib
ENV INSIDE_CONTAINER_FILE_MOUNT=/dk
ENV INSIDE_CONTAINER_FILE_DIRECTORY=docker-share
ENV CONTAINER_INPUT_CONFIG_FILE_NAME=config.json
ENV CONTAINER_OUTPUT_PROGRESS_FILE=ac_progress.json
ENV CONTAINER_OUTPUT_LOG_FILE=ac_logger.log

# Set the default command to execute
ENTRYPOINT python3 -m DKGeneralPurposeContainer
