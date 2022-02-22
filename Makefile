
TAG?=latest
IMAGE_NAME:=dk_general_purpose_container:$(TAG)

all: build

build:
	docker build -f ./Dockerfile -t $(IMAGE_NAME) .
