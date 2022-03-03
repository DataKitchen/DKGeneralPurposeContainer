
TAG?=latest
VERSION?=1.0.0
BASE_IMAGE_NAME:=datakitchenprod/dk_general_purpose_container
DEFAULT_IMAGE_NAME:=$(BASE_IMAGE_NAME):ubuntu20-$(TAG)
VERSIONED_IMAGE_NAME:=$(BASE_IMAGE_NAME):ubuntu20-$(VERSION)


all: build

build:
	docker build -f ./Dockerfile -t $(DEFAULT_IMAGE_NAME) .
	docker tag $(DEFAULT_IMAGE_NAME) $(VERSIONED_IMAGE_NAME)

test:
	IMAGE=$(DEFAULT_IMAGE_NAME) make -C tests test
