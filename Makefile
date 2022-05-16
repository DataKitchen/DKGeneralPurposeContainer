PATH:=bin/:${PATH}
.PHONY: \
    help \
    scan_secrets \
    test unittest imagetest ordertest \
    build \
    tag_latest \
    pull \
    push push_latest \
    rmi rmi_latest


# --- Environment ---

MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MAKEFILE_DIR := $(patsubst %/,%,$(dir $(MAKEFILE_PATH)))
UNITTESTS_DIR := $(MAKEFILE_DIR)/tests

NAMESPACE := datakitchenprod
REPOSITORY := dk_general_purpose_container
IMAGE_PREFIX := $(NAMESPACE)/$(REPOSITORY)
NO_CACHE := --no-cache

ifeq ($(DOCKERFILE), DockerfileUbuntu20Base)
	IMAGE_TAG := ubuntu20-base-$(VERSION)
	IMAGE := $(IMAGE_PREFIX):$(IMAGE_TAG)
	IMAGE_LATEST := $(IMAGE_PREFIX):ubuntu20-base-latest
else ifeq ($(DOCKERFILE), DockerfileUbuntu20)
	IMAGE_TAG := ubuntu20-$(VERSION)
	IMAGE := $(IMAGE_PREFIX):$(IMAGE_TAG)
	IMAGE_LATEST := $(IMAGE_PREFIX):ubuntu20-latest
endif


# --- Helper Functions ---

# Before pushing a new versioned image, ensure one doesn't already exist
image_exists ?= $(shell docker manifest inspect $(IMAGE) > /dev/null; echo $$?)
ensure_new_image = $(if $(value $(image_exists)), $(error Image $(IMAGE) already exists), )

# See https://gist.github.com/bbl/bf4bf5875d0c705c4cd78d264f98a8b1
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))


# --- Help ---

help:
	@echo
	@echo "Utilities:"
	@echo "    scan_secrets      Scan source code for sensitive information"
	@echo
	@echo "Testing:"
	@echo "    test              Run all tests"
	@echo "    unittest          Run unit tests natively"
	@echo "    imagetest         Run unit tests in a Docker container based on DOCKERFILE and VERSION override "
	@echo "                      variables. For example, \"make imagetest VERSION=0.0.1 DOCKERFILE=DockerfileUbuntu20\""
	@echo "                      will run unittests in an image named "
	@echo "                      \"datakitchenprod/dk_general_purpose_container:ubuntu20-0.0.1\""
	@echo "    ordertest         Run the specified DataKitchen order using the specified image version that must be "
	@echo "                      available on Dockerhub. DOCKERFILE and VERSION must be provided to specify the image. "
	@echo "                      USERNAME, PASSWORD, KITCHEN, RECIPE, and VARIATION must be provided to specify the order"
	@echo
	@echo "Build Images:"
	@echo "    build             Build an image based on DOCKERFILE and VERSION override variables. For example, "
	@echo "                      \"make build VERSION=0.0.1 DOCKERFILE=DockerfileUbuntu20\" will create an image "
	@echo "                      tagged with datakitchenprod/dk_general_purpose_container:ubuntu20-0.0.1"
	@echo
	@echo "Tag Images:"
	@echo "    tag_latest        Tag an image based on DOCKERFILE and VERSION override variables. For example,"
	@echo "                      \"make tag_latest VERSION=0.0.1 DOCKERFILE=DockerfileUbuntu20\" will tag the image"
	@echo "                      \"datakitchenprod/dk_general_purpose_container:ubuntu20-0.0.1\" with "
	@echo "                      \"datakitchenprod/dk_general_purpose_container:ubuntu20-latest\""
	@echo "                      Please note, the image you're tagging must already live on the machine where you're "
	@echo "                      executing this command."
	@echo
	@echo "Pull Images:"
	@echo "    pull              Pull an image based on DOCKERFILE and VERSION override variables. For example, "
	@echo "                      \"make pull VERSION=0.0.1 DOCKERFILE=DockerfileUbuntu20\" will pull the image named "
	@echo "                      \"datakitchenprod/dk_general_purpose_container:ubuntu20-0.0.1\" from Dockerhub"
	@echo
	@echo "Push Images:"
	@echo "    push              Push an image to Dockerhub based on DOCKERFILE and VERSION override variables. For "
	@echo "                      example, \"make push VERSION=0.0.1 DOCKERFILE=DockerfileUbuntu20\" will push an image "
	@echo "                      named \"datakitchenprod/dk_general_purpose_container:ubuntu20-0.0.1\" to Dockerhub. "
	@echo "                      The image must already live on the machine where you're executing this command. "
	@echo "    push_latest       Push a latest image to Dockerhub based on DOCKERFILE override variable. For example, "
	@echo "                      \"make push DOCKERFILE=DockerfileUbuntu20)\" will push an image named "
	@echo "                      \"datakitchenprod/dk_general_purpose_container:ubuntu20-latest\" to Dockerhub."
	@echo "                      Please note, the latest image you'r pushing must already live on the machine where "
	@echo "                      you're executing this command."
	@echo
	@echo "Remove Images:"
	@echo "    rmi               Remove a local image based on DOCKERFILE and VERSION override variables. For "
	@echo "                      example, \"make rmi VERSION=0.0.1 DOCKERFILE=DockerfileUbuntu20\" will "
	@echo "                      remove an image named \"datakitchenprod/dk_general_purpose_container:ubuntu20-0.0.1\""
	@echo "    rmi_latest        Remove a local image based on DOCKERFILE and VERSION override variables. For "
	@echo "                      example, \"make rmi_latest VERSION=0.0.1 DOCKERFILE=DockerfileUbuntu20\" will "
	@echo "                      remove an image named \"datakitchenprod/dk_general_purpose_container:ubuntu20-latest\""
	@echo


# --- Utils ---

scan_secrets:
	@./scan_secrets.py src ignored_secrets.txt


# --- Testing ---

test: unittest imagetest ordertest

unittest:
	python3 -m nose unittests

imagetest:
	@:$(call check_defined, VERSION)
	@:$(call check_defined, IMAGE)
	IMAGE=$(IMAGE) make -C tests test

ordertest:
	@:$(call check_defined, VERSION)
	@:$(call check_defined, IMAGE)
	@:$(call check_defined, IMAGE_TAG)
	@:$(call check_defined, USERNAME)
	@:$(call check_defined, PASSWORD)
	@:$(call check_defined, KITCHEN)
	@:$(call check_defined, RECIPE)
	@:$(call check_defined, VARIATION)
	docker run --rm --entrypoint /bin/sh -v $(MAKEFILE_DIR)/run_test_order.py:/dk/run_test_order.py \
	    $(IMAGE) -c "bash; pip3 install DKUtils; python3 run_test_order.py $(USERNAME) $(PASSWORD) $(KITCHEN) $(RECIPE) $(VARIATION) $(IMAGE_TAG)"


# --- Build Images ---

build:
	@:$(call check_defined, VERSION)
	@:$(call check_defined, IMAGE)
	docker build $(NO_CACHE) -f ./$(DOCKERFILE) -t $(IMAGE) .


# --- Tag Images ---

tag_latest: pull
	@:$(call check_defined, VERSION)
	@:$(call check_defined, IMAGE)
	@:$(call check_defined, IMAGE_LATEST)
	docker tag $(IMAGE) $(IMAGE_LATEST)


# --- Pull Images ---

pull:
	@:$(call check_defined, VERSION)
	@:$(call check_defined, IMAGE)
	docker pull $(IMAGE)


# --- Push Images ---

push: 
	@:$(call check_defined, VERSION)
	@:$(call check_defined, IMAGE)
	@:$(call ensure_new_image)
	docker push $(IMAGE)

push_latest:
	@:$(call check_defined, IMAGE_LATEST)
	docker push $(IMAGE_LATEST)


# --- Remove Images ---

rmi:
	@:$(call check_defined, VERSION)
	@:$(call check_defined, IMAGE)
	docker rmi $(IMAGE)

rmi_latest:
	@:$(call check_defined, VERSION)
	@:$(call check_defined, IMAGE_LATEST)
	docker rmi $(IMAGE_LATEST)
