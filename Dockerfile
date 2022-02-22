#@IgnoreInspection BashAddShebang
############################################################
# DKGeneralPurposeContainer
# Dockerfile to build Analytic Container Template
############################################################

FROM datakitchenprivate/dk_analytic_container_base:latest as source
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
    build-essential \
    python-distribute\
    python3 \
    python3-dev \
    python3-pip

# Set the default directory where CMD will execute
WORKDIR /dk

# Copy gpc stuff
COPY ./requirements-ubuntu.txt /dk/requirements.txt
COPY ./requirements-common.txt /dk/requirements-common.txt
COPY ./README.md                        /dk/README.md
COPY ./icon.svg                         /dk/icon.svg

# Install python dependencies
RUN pip3 install --upgrade --ignore-installed --requirement /dk/requirements.txt

RUN rm -f /dk/requirements*.txt

# copy analytic container python files
COPY --from=source /dk/lib              /dk/lib
COPY ./src /dk/lib/gpc

ENV PYTHONPATH=/dk/lib

# Set the default command to execute
ENTRYPOINT python3 -m gpc.DKGeneralPurposeContainer
