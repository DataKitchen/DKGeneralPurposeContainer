# Project Description

## Description
This project is used to build General Purpose Container (GPC) images for use in DataKitchen Platform Docker container 
nodes. These images in, conjunction with the DataKitchen Platform, run shell scripts, python3 code, and Jupyter 
notebooks. This facilitates the automation of virtually any current or future tool from within the DataKitchen Platform.

## Images
Currently, only Ubuntu based images are provided. However, other base images could be used as well. For instance, an
Amazon Linux 2 base image was built and tested and could be made available if desired.

## Repository
[DKGeneralPurposeContainer](https://github.com/DataKitchen/DKGeneralPurposeContainer)

## Build
As of this writing, there are 2 Dockerfiles available for building the GPC. The first is DockerfileUbuntu20Base which
builds a base image that contains a minimum set of APT and python packages. This image can run simple shell 
and python scripts. It can also be used as a base image for building custom GPC images with packages and configuration 
specific to an organization or project. The second is DockerfileUbuntu20 which inherits from the base image and adds 
APT and python packages deemed useful for automating tools from within the DataKitchen Platform. Customers are 
encouraged to build their own custom image (or base image, if need be) containing the suite of tools required by their
organiziation or project teams. 

The DOCKERFILE variable assignment below tells Make which Dockerfile to build. The VERSION variable assignment tells
Make how to tag the created image. It is highly recommended to use semantic versions when building your images.

```bash
make build DOCKERFILE=<dockerfile> VERSION=<semantic_version>
```
example:
```
make build DOCKERFILE=DockerfileUbuntu20 VERSION=0.0.1
```
\* By default, the images are built with the `--no-cache` option (i.e. `NO_CACHE=--no-cache`). To disable this option, 
add `NO_CACHE=` to the make command above.

## Deploy
By default, the Makefile deploys the image to DataKitchen's private repository on Dockerhub in the _datakitchenprod_ 
namespace and _dk_general_purpose_container_ repository. To customize the destination of the images, users may provide 
`REGISTRY_LOCATION`, `NAMESPACE`, and `REPOSITORY` variable assignments when issuing a Makefile command. For 
instance, to push to a registry other than Dockerhub, set `REGISTRY_LOCATION` with the address and port of the registry,
making sure to include the trailing slash (e.g. my.registry.address:port/). Currently, the versioned tag is either 
`ubuntu20-base-<VERSION>` for DockerfileUbuntu20Base and `ubuntu20-<VERSION>` for DockerfileUbuntu20. The tags 
for the two images are _datakitchenprod/dk_general_purpose_container:ubuntu20-base-<VERSION>_ and 
_datakitchenprod/dk_general_purpose_container:ubuntu20-<VERSION>_ (i.e. `REGISTRY_LOCATION` is empty by default). If
`REGISTRY_LOCATION` was set to `my.registry.address:port/`, the tag would be:
_my.registry.address:port/datakitchenprod/dk_general_purpose_container:ubuntu20-base-<VERSION>_)

```bash
make push DOCKERFILE=<dockerfile> VERSION=<semantic_version>
```

Typically, users will want to test and validate this versioned image before tagging it with latest and pushing it. The
`tag_latest` and `push_latest` targets are for this very purpose. The commands below will tag the image defined by 
DOCKERFILE and VERSION with latest (i.e. `ubuntu20-base-latest` or `ubuntu20-latest`) and then push that image. The 
`tag_latest` target performs a pull before the tag to ensure the image exists locally.
```bash
make tag_latest DOCKERFILE=<dockerfile> VERSION=<semantic_version>
make push DOCKERFILE=<dockerfile> VERSION=<semantic_version>
```

## Testing
Three make targets exist to run tests: unittest, imagetest, and ordertest. The unittest target runs locally (i.e. not
in a Docker container) to test the Analytic Container source code. By the way, this code lives in the src directory and
is executed via the ENTRYPOINT to container. Therefore, if this code is changed, ensure the unittests pass. The 
imagetest target runs a test inside a Docker container, similar to how container nodes are executed in the DataKitchen
Platform. This test will run the local image specified by the DOCKERFILE and VERSION variables. Therefore, you can build
the image locally and test it before pushing to Dockerhub. Finally, the ordertest target runs an Order in the 
DataKitchen platform using the new image specified by the DOCKERFILE and VERSION variables. However, the image must be
pushed and available on Dockerhub so the platform can pull it and run it.

## CI/CD
The Makefile targets are intended to facilitate a CI/CD pipeline for deploying new GPC images. Internally, DataKitchen's
CI/CD pipeline does the following:
* Run unit tests (make unittest)
* Build a new versioned image (make build DOCKERFILE=$DOCKERFILE VERSION=$VERSION)
* Run image tests (make imagetest DOCKERFILE=$DOCKERFILE VERSION=$VERSION)
* Push the versioned image to Dockerhub (make push DOCKERFILE=$DOCKERFILE VERSION=$VERSION)
* Run order tests (make ordertest VERSION=$VERSION DOCKERFILE=$DOCKERFILE USERNAME=<> PASSWORD=<> KITCHEN=<> RECIPE=<> VARIATION=<>)
* Tag the versioned image as latest (make tag_latest DOCKERFILE=$DOCKERFILE VERSION=$VERSION)
* Push the latest image (make push_latest DOCKERFILE=$DOCKERFILE VERSION=$VERSION)


## Ubuntu20 Changelog

### 0.0.3 - 2022-07-13
* Update DKUtils to v2.5.0


### 0.0.2 - 2022-05-31
* Added APT packages
  * git
  * libxml2-dev
  * libxslt1-dev
  * nano
  * rsync
  * wget
* Update psycopg2 to v2.9.3 and remove `--no-binary` option (see [Change in binary packages between Psycopg 2.7 and 2.8](https://www.psycopg.org/docs/install.html#change-in-binary-packages-between-psycopg-2-7-and-2-8))
* Added traitlets<=5.2.0 to requirements to resolve AssertionError with latest version 5.2.2

### 0.0.1 - 2022-05-26
* Initial release


## Ubuntu20 Base Changelog

### 0.0.1 - 2022-05-26
* Initial release

