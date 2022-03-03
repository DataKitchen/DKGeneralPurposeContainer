import logging

# ---------------------------------------------------------------------------------------------------------------------
# config file keys
# ---------------------------------------------------------------------------------------------------------------------
CONFIG_KEYS = 'keys'
CONFIG_SCRIPT = 'script'
CONFIG_PARAMETERS = 'parameters'
CONFIG_ENVIRONMENT = 'environment'
CONFIG_APT_DEPENDENCIES = 'apt-dependencies'
CONFIG_YUM_DEPENDENCIES = 'yum-dependencies'
CONFIG_DEPENDENCIES = 'dependencies'
CONFIG_ASSIGN = 'assign'
CONFIG_EXPORT = 'export'
CONFIG_INDEX_URL = 'index-url'
# ---------------------------------------------------------------------------------------------------------------------
# logging
# ---------------------------------------------------------------------------------------------------------------------
AC_LOGGING = logging.INFO
AC_LOG_FILE_LOCATION = './docker-share/ac_logger.log'
AC_APPEND_MODE = 'a+'
AC_WRITE_MODE = 'w'

# ---------------------------------------------------------------------------------------------------------------------
# k8s secrets
# ---------------------------------------------------------------------------------------------------------------------
K8S_SECRETS_BASE_PATH = '/etc/datakitchen/.secrets'

# ---------------------------------------------------------------------------------------------------------------------
# Input environment variables
# ---------------------------------------------------------------------------------------------------------------------
CONTAINER_INPUT_CONFIG_FILE_PATH = 'CONTAINER_INPUT_CONFIG_FILE_PATH'
CONTAINER_INPUT_CONFIG_FILE_NAME = 'CONTAINER_INPUT_CONFIG_FILE_NAME'
CONTAINER_INPUT_CONFIG_FILE_NAME = 'CONTAINER_INPUT_CONFIG_FILE_NAME'
CONTAINER_OUTPUT_PROGRESS_FILE = 'CONTAINER_OUTPUT_PROGRESS_FILE'
CONTAINER_OUTPUT_LOG_FILE = 'CONTAINER_OUTPUT_LOG_FILE'
CONTAINER_OUTPUT_FILE = 'CONTAINER_OUTPUT_FILE'
INSIDE_CONTAINER_FILE_MOUNT = 'INSIDE_CONTAINER_FILE_MOUNT'
INSIDE_CONTAINER_FILE_DIRECTORY = 'INSIDE_CONTAINER_FILE_DIRECTORY'

CONTAINER_REQUIRED_ENVIRONMENT_VARS = [
    INSIDE_CONTAINER_FILE_MOUNT, INSIDE_CONTAINER_FILE_DIRECTORY, CONTAINER_INPUT_CONFIG_FILE_NAME,
    CONTAINER_OUTPUT_PROGRESS_FILE, CONTAINER_OUTPUT_LOG_FILE
]
"""
 --------------------------------------------------------------------------------
 ENV Variables:

 CONTAINER_INPUT_CONFIG_FILE_PATH:
    command line:   /vagrant/AnalyticContainers/ACBase/docker-share
    container:      docker-share
    node:           /container-node/docker-share
 CONTAINER_INPUT_CONFIG_FILE_NAME
    command line:   config.json
    container:      config.json
    node:           config.json
 CONTAINER_OUTPUT_PROGRESS_FILE
    command line:   progress.json
    container:      progress.json
    node:           progress.json
 CONTAINER_OUTPUT_LOG_FILE
    command line:   ams_logger.log
    container:      ams_logger.log
    node:           ams_logger.log
 INSIDE_CONTAINER_FILE_MOUNT
    command line:   /vagrant/AnalyticContainers/ACBase
    container:      /ACBase
    node:           /ACBase
 INSIDE_CONTAINER_FILE_DIRECTORY
    command line:   docker-share
    container:      docker-share
    node:           docker-share
"""
# --------------------------------------------------------------------------------
# Return Status of Execution (place in progress.json at top level)
# --------------------------------------------------------------------------------
CONTAINER_RETURN_STATUS = 'container-return-status'
CONTAINER_STATUS_SUCCESS = 'completed_success'  # -- all complete, go on to data sinks
CONTAINER_STATUS_ERROR = 'error'  # -- somethings wrong, stop processing
CONTAINER_STATUS_CONTINUE = 'continue_production'  # -- all good, but need to try again later
ALLOWED_CONTAINER_RETURN_STATUSES = [
    CONTAINER_STATUS_SUCCESS, CONTAINER_STATUS_ERROR, CONTAINER_STATUS_CONTINUE
]

# ---------------------------------------------------------------------------------------------------------------------
# Tests (place in progress.json at top level)
# ---------------------------------------------------------------------------------------------------------------------
# for each test, below is how to add them to the progress.json
#  test_key (i.e. the test name
#  test data is a dict() containing several items for each test_key
#       CONTAINER_TEST_RESULT = Result of the test: ALLOWED_CONTAINER_TEST_RESULTS
#       CONTAINER_TEST_DATETIME = string datetime (always of last time this dict was set)
#       CONTAINER_TEST_LOGIC  = (string explaining test logic)
#       CONTAINER_TEST_ACTION = What the test is supposed to do -- desired action: ALLOWED_CONTAINER_TEST_ACTIONS
#       CONTAINER_TEST_VALUE_TYPE = The type of the data: ALLOWED_CONTAINER_TEST_TYPES
#       CONTAINER_TEST_VALUE = dict containing all the test variable names and values
#                   test variable name   (e.g. 'sql-data01-size'): list of values (of type ALLOWED_CONTAINER_TEST_TYPES)
#                   test variable name 2 (e.g. 'ftp-data02-size'): list of values (of type ALLOWED_CONTAINER_TEST_TYPES)
# ---------------------------------------------------------------------------------------------------------------------

CONTAINER_TEST_DATA = 'test-data'
# per test data
CONTAINER_TEST_RESULT = 'test-result'
CONTAINER_TEST_DATETIME = 'test-datetime'
CONTAINER_TEST_LOGIC = 'test-logic'
CONTAINER_TEST_ACTION = 'test-action'
CONTAINER_TEST_VALUE_TYPE = 'test-value-type'
CONTAINER_TEST_VALUE = 'test-value'
# Test Results
CONTAINER_TEST_RESULT_FAILED = 'TestFailed'
CONTAINER_TEST_RESULT_PASSED = 'TestPassed'
CONTAINER_TEST_RESULT_WARNING = 'TestWarning'
ALLOWED_CONTAINER_TEST_RESULTS = [
    CONTAINER_TEST_RESULT_FAILED, CONTAINER_TEST_RESULT_PASSED, CONTAINER_TEST_RESULT_WARNING
]
# Desired Action for each test
CONTAINER_TEST_ACTION_LOG = 'log'
CONTAINER_TEST_ACTION_WARNING = 'warning'
CONTAINER_TEST_ACTION_STOP_ON_ERROR = 'stop-on-error'
ALLOWED_CONTAINER_TEST_ACTIONS = [
    CONTAINER_TEST_ACTION_LOG, CONTAINER_TEST_ACTION_WARNING, CONTAINER_TEST_ACTION_STOP_ON_ERROR
]
# test data types
CONTAINER_TEST_VALUE_INT = 'type-int'
CONTAINER_TEST_VALUE_STRING = 'type-string'
CONTAINER_TEST_VALUE_FLOAT = 'type-float'
CONTAINER_TEST_VALUE_DATE = 'type-date'
CONTAINER_TEST_VALUE_UNKNOWN_TYPE = 'type-unknown'
ALLOWED_CONTAINER_TEST_TYPES = [
    CONTAINER_TEST_VALUE_INT, CONTAINER_TEST_VALUE_STRING, CONTAINER_TEST_VALUE_FLOAT,
    CONTAINER_TEST_VALUE_DATE, CONTAINER_TEST_VALUE_UNKNOWN_TYPE
]
