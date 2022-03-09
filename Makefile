
VERSION?=latest
IMAGE_NAME:=datakitchenprod/dk_general_purpose_container
TMP_IMAGE_NAME:=$(IMAGE_NAME):ubuntu20-base-dev
BASE_IMAGE_NAME:=$(IMAGE_NAME):ubuntu20-base-$(TAG)
FULL_IMAGE_NAME=$(IMAGE_NAME):ubuntu20-$(TAG)


all: unittest build_ubuntu20_base imagetest build_ubuntu20

build_ubuntu20_base:
	docker build -f ./DockerfileUbuntu20Base -t $(TMP_IMAGE_NAME) .

build_ubuntu20:
	docker tag $(TMP_IMAGE_NAME) $(BASE_IMAGE_NAME)
	docker build --build-arg BASE_IMAGE=$(BASE_IMAGE_NAME) -f ./DockerfileUbuntu20 -t $(FULL_IMAGE_NAME) .

test: unittest imagetest

imagetest:
	IMAGE=$(TMP_IMAGE_NAME) make -C tests test

unittest:
	nosetests unittests


push_test: 
	docker push $(TMP_IMAGE_NAME)

push: 
	docker push $(BASE_IMAGE_NAME)
	docker push $(FULL_IMAGE_NAME)
