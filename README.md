# Project Description

## Description
This project is a general purpose container to run shell scripts and python3 scripts. It can be used as a base or reference design to simplify custom container builds.

## Images
Both Ubuntu based and Amazon Linux 2 based images are provided. The Amazon Linux 2 based image is available using the tag `amzlx`. The major difference is the Amazon Linux 2 image does not run as the `root` user and instead runs as the `datakitchen` user with UID/GID 1006/1007.

## Repository
https://ghe.datakitchen.io/DataKitchen/AnalyticContainer

## Command to build the image
```bash
cd <DKROOT>/AnalyticContainer/DKGeneralPurposeContainer
bash run.sh <image base name> <semantic version>
```
examples:
```
bash run.sh ubuntu20 x.y.z

bash run.sh -n amzlx x.y.z
```
\*-n option adds --no-cache to docker build command

## To deploy
```bash
docker login -u dkimplementation -p "<password>" 
docker push datakitchenprod/dk_general_purpose_container:x.y.z
docker push datakitchenprod/dk_general_purpose_container:latest
```
or
```bash
docker login -u dkimplementation -p "<password>" 
docker push datakitchenprod/dk_general_purpose_container:amzlx-x.y.z
docker push datakitchenprod/dk_general_purpose_container:amzlx-latest
```

## Docker image name
dk_general_purpose_container

## To run tests
In `/dk` path, clone or pull repos `DKAnalyticContainer` and `AnalyticContainer`:
``` bash
cd /dk/AnalyticContainer/DKGeneralPurposeContainer/tests
export PYTHONPATH=/dk
python3 TestContainer.py
```

## Container details
* Image uses Python3 exclusively.
* Supports shell scripts, Python3 scripts, and Jupyter Notebooks.
* Supports a subset of methods from the Python3 logger. See section below.
* Includes several pre-installed apt-get and Python tools. See section below.
* Sets a standard structure for passing parameters and variables, installing dependencies, retrieving files, and logging without requiring significant custom code.

### Python script exit code procedure

* To make your python script consistently return an exit code
``` bash
global HELPERS


if __name__ == "__main__":
    exitcode = 3
    HELPERS.exit(exitcode)

```


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


## Changelog

### 2.10.0 - 2021-04-09
* Update DKUtils from v1.8.2 to v1.10.0

### 2.9.0 - 2021-03-15
* Create new GPC from scratch to update apt packages and resolve apt-get install issues

### 2.8.1 - 2021-02-25
* Update DKUtils to v1.8.2

### 2.8.0 - 2021-02-18
* Update cryptography and pyyaml libraries to address CVEs
* Amazon Linux 2 specific changes
    * Due to an incompatibilites with library updates, the awscli & azure-cli were removed from the Amazon 
    Linux 2 image
    * Pip required updating to v21.0.1 to handle latest pyyaml version
    * Pip installs now include the --user flag (installed to ~/.local)
* Update DKUtils to v1.8.0

### 2.7.0 - 2021-02-16
* Add python script exit code handling. For details check "Python script exit code procedure" above

### 2.6.0 - 2021-02-11
* Update DKUtils to v1.7.0

### 2.5.0 - 2021-02-08
* Add yum upgrade, autoremove, and clean as well as removing /var/cache/yum

### 2.4.0 - 2021-02-08
* Update DKUtils to v1.6.0

### 2.3.0 - 2021-02-02
* Update DKUtils to v1.3.2

### 2.2.0 - 2021-02-01
* Add Amazon Linux 2 Based image

### 2.1.0 - 2021-01-08
* Add libxml2-dev and libxslt1-dev apt packages that caused some pip installs 
  to fail (e.g. nipyapi) after migration from ubuntu 19.04 to 20.04.

### 2.0.2 - 2020-12-15
* Updated image to ubuntu:20.04
* Added SQLAlchemy Python package
* Added rsync package from Apt

### 2.0.1 - 2020-11-18
* Updated image to use UTF-8 encoding
* Added DKUtils python package

### 2.0.0 - 2020-09-17
* Updated base image to ubuntu:19.10
* Updated dependencies in requirements.txt to latest versions
* Updated strict versioning to minimum versioning in requirements.txt
* Missing Jupyter package is now caught and clearly logged

### 1.8.0 - 2020-09-14
* Enhanced configuration (`config.json`) validation checks in GPC.

### 1.7.0 - 2020-03-11
* Fixed log output from apt + pip instllations in GPC.

### 1.6.0 - 2020-03-02
* Fixed log items from shell script output in GPC.

### 1.5.0 - 2020-02-17
* Added a check for cases in which vault secrets are being used directly in scripts.
This is not allowed for security reasons. The recommended procedure is to use "parameters" in config.json instead.
Example:
    "keys": {
        "run-script": {
            "script": "test.ipynb",
            "parameters": {
                "param1": "#{vault://param1}"
            }
        }
    }

### 1.4.1 - 2019-12-09
* python libraries included: tableauserverclient==0.9

### 1.4.0 - 2019-11-04
* Added compatibility with Kubernetes Secrets.

### 1.3.1 - 2019-10-08
* Do not remove package lists from Docker image - this breaks user defined apt-get installs.

### 1.3.0 - 2019-10-07
* Added support for Jupyter Notebooks
* Update Dockerfile based on [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
* Alphebetized requirements.txt
* Added markdown to this README

### 1.2.1 - 2019-09-19
* Installed pip dependency xlrd==1.1.0 (needed for pandas to work properly)

### 1.2.0 - 2019-09-12
* Refactor to use python3
* Refactor container name to dk_general_purpose_container (previously was ac_container_template)

### 1.1.3 - 2019-09-12
* python libraries removed: boxsdk[jwt]

### 1.1.2 - 2019-09-11
* include feature to install apt and pip dependencies in config.json. For example:
```json
{
    "apt-dependencies": [
      "curl", "nano"
    ],
    "dependencies": [
      "DKCloudCommand", "boxsdk[jwt]"
    ],
    "keys": {
        ...
    }
}
```

* python libraries included: azure-cli, awscli, requests==2.22.0
* python libraries removed: DKCloudCommand (we will use rest api instead)

### 1.1.1 - 2019-09-11
* python libraries included: google-cloud-bigquery, google-cloud-storage

### 1.1.0 - 2019-09-10
* Add unit tests
* Python and shell script auto detection.
* New Os environment variables feature, through the use of:
```json
    {
        "keys" : {
            "key" : {
                "script" : "env_variables.py",
                "environment": {
                    "env_variable_0": "I am a string",
                    "env_variable_1": 45
                }
           }
        }
    }
```    
* DKCloudCommand package included
* python libraries included: boto, paramiko, pandas, numpy, psycopg2, salesforce

### 1.0.0 - 2019-06-14
* Initial version
