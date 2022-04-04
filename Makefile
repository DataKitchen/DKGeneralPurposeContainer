
VERSION?=latest
IMAGE_NAME:=datakitchenprod/dk_general_purpose_container
BASE_IMAGE_NAME:=$(IMAGE_NAME):ubuntu20-base-$(VERSION)
BASE_TMP_IMAGE_NAME:=$(IMAGE_NAME):ubuntu20-base-dev
FULL_IMAGE_NAME=$(IMAGE_NAME):ubuntu20-$(VERSION)
TMP_IMAGE_NAME:=$(IMAGE_NAME):ubuntu20-dev


all: unittest build_ubuntu20_base imagetest build_ubuntu20

build_ubuntu20_base:
	docker build -f ./DockerfileUbuntu20Base -t $(BASE_TMP_IMAGE_NAME) .

build_ubuntu20:
	docker build --build-arg BASE_IMAGE=$(BASE_IMAGE_NAME) -f ./DockerfileUbuntu20 -t $(TMP_IMAGE_NAME) .

test: unittest imagetest

imagetest_base:
	IMAGE=$(BASE_TMP_IMAGE_NAME) make -C tests test

imagetest:
	IMAGE=$(TMP_IMAGE_NAME) make -C tests test

unittest:
	python3 -m nose unittests


push_test: 
	docker push $(TMP_IMAGE_NAME)

push_test_base: 
	docker push $(BASE_TMP_IMAGE_NAME)

push: 
	docker tag $(TMP_IMAGE_NAME) $(FULL_IMAGE_NAME)
	docker push $(FULL_IMAGE_NAME)

push_base:
	docker tag $(BASE_TMP_IMAGE_NAME) $(BASE_IMAGE_NAME)
	docker push $(BASE_IMAGE_NAME)
