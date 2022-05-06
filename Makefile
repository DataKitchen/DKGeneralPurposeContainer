
VERSION?=latest
IMAGE_NAME:=datakitchenprod/dk_general_purpose_container
BASE_IMAGE_NAME:=$(IMAGE_NAME):ubuntu20-base-$(VERSION)
BASE_TMP_IMAGE_NAME:=$(IMAGE_NAME):ubuntu20-base-dev
FULL_IMAGE_NAME=$(IMAGE_NAME):ubuntu20-$(VERSION)
TMP_IMAGE_NAME:=$(IMAGE_NAME):ubuntu20-dev


# --- Help ---

help:
	@echo
	@echo "Utilities:"
	@echo "    scan_secrets scan source code for sensitive information"
	@echo
	@echo "Testing:"
	@echo "    test              run all tests"
	@echo "    imagetest_base    "
	@echo "    imagetest         "
	@echo "    unittest          "
	@echo "    imagetest         "
	@echo "    push_test         "
	@echo "    push_test_base    "
	@echo
	@echo "Build Images:"
	@echo "    build_ubuntu20_base  "
	@echo "    build_ubuntu20       "
	@echo
	@echo "Push Images:"
	@echo "    push            "
	@echo "    push_base       "
	@echo


# --- Utils ---

scan_secrets:
	@./scan_secrets.py src ignored_secrets.txt


# --- Testing ---

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


# --- Build Images ---

build_ubuntu20_base:
	docker build -f ./DockerfileUbuntu20Base -t $(BASE_TMP_IMAGE_NAME) .

build_ubuntu20:
	docker build --build-arg BASE_IMAGE=$(BASE_IMAGE_NAME) -f ./DockerfileUbuntu20 -t $(TMP_IMAGE_NAME) .


# --- Push Images ---

push: 
	docker tag $(TMP_IMAGE_NAME) $(FULL_IMAGE_NAME)
	docker push $(FULL_IMAGE_NAME)

push_base:
	docker tag $(BASE_TMP_IMAGE_NAME) $(BASE_IMAGE_NAME)
	docker push $(BASE_IMAGE_NAME)
