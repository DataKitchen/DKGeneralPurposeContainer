# Project Description

## Description
This project is used to build General Purpose Container (GPC) images for use in DataKitchen Platform Docker container 
nodes. These images in conjunction with the DataKitchen Platform will run shell scripts, python3 code, and Jupyter 
notebooks. It facilitates the automation of virtually any current or future tool from within the DataKitchen Platform.

## Images
Both Ubuntu based and Amazon Linux 2 based images are provided. The Amazon Linux 2 based image is available using the 
tag `amzlx`. The major difference is the Amazon Linux 2 image does not run as the `root` user and instead runs as the 
`datakitchen` user with UID/GID 1006/1007.

## Repository
https://github.com/DataKitchen/DKGeneralPurposeContainer

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
\* By default, the images are built with the --no-cache option (i.e. `NO_CACHE=--no-cache`). To disable this option, add 
`NO_CACHE=` to the make command above.

## Deploy
By default, the Makefile deploys the image to DataKitchen's private repository on Dockerhub in the _datakitchenprod_ 
namespace and _dk_general_purpose_container_ repository. Users may provide alternative `NAMESPACE` and `REPOSITORY`
variable assignments via the provided Makefile commands if they so choose. However, users
must update the Makefile to push to a different registry other than Dockerhub. Currently, the versioned tag is either 
`ubuntu20-base-<VERSION>` for DockerfileUbuntu20Base and `ubuntu20-<VERSION>` for DockerfileUbuntu20. The full image 
paths for the two images are _datakitchenprod/dk_general_purpose_container:ubuntu20-base-<VERSION>_ and 
_datakitchenprod/dk_general_purpose_container:ubuntu20-<VERSION>_.

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


## Container details
* Image uses Python3 exclusively.
* Supports shell scripts, Python3 scripts, and Jupyter Notebooks.
* Supports a subset of methods from the Python3 logger. See section below.
* Includes several pre-installed apt-get and Python tools. See section below.
* Sets a standard structure for passing parameters and variables, installing dependencies, retrieving files, and logging without requiring significant custom code.

### Logger methods supported
* Printing to logs using LOGGER.info()
* **LOGGER.setLevel()**, where the default level is warning. This method requires import logging in script to change the default level.

  Example:
``` bash
        LOGGER.setLevel(logging.DEBUG)
```
* Alternate logging levels.
``` bash
        LOGGER.debug()
        LOGGER.warning()
        LOGGER.error()
        LOGGER.critical()
```

### Pre-installed packages

#### Standard Ubuntu Image
| apt-get tools   	|                 	|                   	|             	|
|:-----------------	|-----------------	|-------------------	|-------------	|
| build-essential 	| freetds-dev     	| nano              	| python3-pip 	|
| curl            	| git             	| net-tools         	| rsync       	|
| dialog          	| gpgv            	| python-distribute 	| tar         	|
| emacs           	| libncurses5-dev 	| python3           	| wget         	|
| freetds-bin     	| libpq-dev       	| python3-dev       	| jq          	|

#### Amazon Linux 2 Image
| yum tools             |                       |                       |                    |
|:----------------------|-----------------------|-----------------------|--------------------|
| epel                  | emacs                 | freetds-devel         | nano               |
| sudo                  | git                   | gnupg2                | tar                |
| shadow-utils          | net-tools             | rsync                 | python3            |
| curl                  | make                  | wget                  | python3-pip        |
| dialog                | freetds               | jq                    | python3-setuptools |
| ncurses-devel         | libxslt-devel         | postgresql-devel      | python3-devel      |
| gcc                   | gcc-c++               |                       |                    |

#### All Images
| python packages                   |                                       |                               |
|:----------------------------------|---------------------------------------|-------------------------------|
| awscli>=1.18.137\*                | google-cloud-storage>=1.31.0          | scikit-learn>=0.23.2          |
| azure-cli>=2.11.1\*               | jupyter>=1.0.0                        | scipy>=1.5.2                  |
| beautifulsoup4>=4.9.1             | oauth2client>=4.1.3                   | setuptools>=50.3.0            |
| boto>=2.49.0                      | openpyxl>=3.0.5                       | simple-salesforce>=1.10.1     |
| boto3>=1.14.60                    | matplotlib>=3.3.1                     | six>=1.15.0                   |
| cryptography>=3.4.5\*             | numpy>=1.19.2                         | sqlalchemy==1.3.18            |
| Cython>=0.28.5                    | pandas>=1.1.2                         | xlrd>=1.2.0                   |
| DKUtils>=1.10.0                   | paramiko>=2.7.2                       | tableauserverclient>=0.13     |
| google-api-python-client>=1.12.1  | psycopg2>=2.8.6 --no-binary psycopg2  |                               |
| google-cloud>=0.34.0              | pyyaml>=5.4.1                         |                               |
| google-cloud-bigquery>=1.27.2     | requests>=2.24.0                      |                               |

\*Not installed in Amazon Linux 2 image


## Ubuntu20 Changelog

### 0.0.1 - 2022-05-26
* Initial release


## Ubuntu20 Base Changelog

### 0.0.1 - 2022-05-26
* Initial release

