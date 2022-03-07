
TAG?=latest
VERSION?=1.0.0
BASE_IMAGE_NAME:=datakitchenprod/dk_general_purpose_container
DEFAULT_IMAGE_NAME:=$(BASE_IMAGE_NAME):ubuntu20-base-$(TAG)
VERSIONED_IMAGE_NAME:=$(BASE_IMAGE_NAME):ubuntu20-base-$(VERSION)


all: build_ubuntu20_base test

build_ubuntu20_base:
	docker build -f ./DockerfileUbuntu20Base -t $(DEFAULT_IMAGE_NAME) .

test:
	IMAGE=$(DEFAULT_IMAGE_NAME) make -C tests test


push-default: test
	docker push $(DEFAULT_IMAGE_NAME)

push: test
	docker tag $(DEFAULT_IMAGE_NAME) $(VERSIONED_IMAGE_NAME)
	docker push $(VERSIONED_IMAGE_NAME)
