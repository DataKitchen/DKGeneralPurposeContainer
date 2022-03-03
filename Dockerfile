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

RUN apt-get update && \
    apt-get install sudo

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends tzdata

# Install basic applications
RUN sudo apt-get update && sudo apt-get install --yes \
    python3 \
    python3-pip

# Set the default directory where CMD will execute
WORKDIR /dk

# Copy gpc stuff
COPY ./icon.svg                         /dk/icon.svg

COPY ./src /dk/lib

ENV PYTHONPATH=/dk/lib

# Set the default command to execute
ENTRYPOINT python3 -m DKGeneralPurposeContainer
