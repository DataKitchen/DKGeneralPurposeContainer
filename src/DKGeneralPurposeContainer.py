import os
import runpy
import subprocess
import traceback

from datetime import datetime
from uuid import uuid4

from AnalyticContainerLibrary.ACBase import ACHelpers, ACLogger, ACBase
from AnalyticContainerLibrary.ACSettings import (
    CONTAINER_STATUS_SUCCESS,
    CONTAINER_STATUS_ERROR,
    CONFIG_APT_DEPENDENCIES,
    CONFIG_YUM_DEPENDENCIES,
    CONFIG_ASSIGN,
    CONFIG_DEPENDENCIES,
    CONFIG_ENVIRONMENT,
    CONFIG_EXPORT,
    CONFIG_KEYS,
    CONFIG_PARAMETERS,
    CONFIG_SCRIPT,
)

JUPYTER_UNAVAILABLE = False
try:
    import nbformat
    from nbconvert import PythonExporter
except Exception as e:
    JUPYTER_UNAVAILABLE = True
    ACLogger.log_and_print("Jupyter disabled - required packages not installed.")


class DKGeneralPurposeContainer(ACBase):
    def run(self):
        try:
            # log start and timestamp
            ACLogger.log_and_print("Starting...")

            # add start timestamp to progress file
            self.set_progress("start-time", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

            # check container config is ok
            config_valid, validation_errors = self.valid_config()
            if not config_valid or validation_errors:
                validation_error_message = "Invalid Config: "
                if len(validation_errors) > 1:
                    validation_error_message += ", ".join(validation_errors)
                else:
                    validation_error_message += validation_errors[0]
                self.print_container_state()
                raise Exception(validation_error_message)

            package_manager = self.determine_package_manager()
            if package_manager == "apt":
                self.install_apt_dependencies(self.configuration.get(CONFIG_APT_DEPENDENCIES, []))
                user = False
            elif package_manager == "yum":
                self.install_yum_dependencies(self.configuration.get(CONFIG_YUM_DEPENDENCIES, []))
                user = True

            # install pip packages
            self.install_pip_dependencies(self.configuration.get(CONFIG_DEPENDENCIES, []), user=user)

            # run keys
            for key, value in self.configuration[CONFIG_KEYS].items():
                self.run_key(key, value)

            # set container status as success
            self.set_container_status(CONTAINER_STATUS_SUCCESS)
        except Exception as e:
            # we had an error, log the stack trace and set container status as error
            ACLogger.log_and_print_error(
                "DKGeneralPurposeContainer Container: Error %s - %s" % (str(e), traceback.format_exc())
            )
            self.set_container_status(CONTAINER_STATUS_ERROR)
        finally:
            # we are done, log end timestamp write the log and progress file
            self.set_progress("end-time", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            self.write_log()
            self.write_progress()

    def valid_config(self):
        validation_errors = []
        # ensure configuration is not empty/missing
        if not self.configuration:
            validation_errors.append("empty or missing configuration")
        # ensure CONFIG_KEYS exists in configuration
        elif CONFIG_KEYS not in self.configuration:
            validation_errors.append("empty or missing configuration keys")
        # ensure CONFIG_KEYS in configuraiton is a dictionary
        elif not isinstance(self.configuration[CONFIG_KEYS], dict):
            validation_errors.append("invalid or wrong configuration type")
        # ensure all CONFIG_KEY scripts are not empty/missing
        if not validation_errors:
            for key, key_data in self.configuration[CONFIG_KEYS].items():
                if len(key_data[CONFIG_SCRIPT]) == 0:
                    validation_errors.append("empty or missing configuration script key")
        # in here you can define what is a valid configuration for your analytic container
        my_configuration_check = True
        # in here you are including base class validations as well
        validation = my_configuration_check and self.valid_configuration
        return validation and not validation_errors, validation_errors

    def run_key(self, key, key_data):
        # get a particular attribute from within the key, can be anything, in this case a script name
        script = key_data[CONFIG_SCRIPT]

        # load variables to be injected as environment variables
        env_variables = key_data.get(CONFIG_ENVIRONMENT, {})
        for k, v in env_variables.items():
            os.environ[k] = str(v)

        # Get Parameters
        parameters = key_data.get(CONFIG_PARAMETERS, {})
        parameters = ACHelpers.resolve_vault_references(parameters)

        # Get list of variables to be exported
        exported_vars = key_data.get(CONFIG_EXPORT, [])

        # Get assignments (files which will be mapped into runtime variables)
        assignments = key_data.get(CONFIG_ASSIGN, {})

        # Check vault values are not present inside the script (which is not allowed for security reasons)
        self.check_vault_not_present(key, script)

        # run script
        ACLogger.log_and_print("Running key %s - Script: %s" % (key, script))
        if script.endswith(".ipynb"):
            self.run_jupyter_notebook(key, script, parameters, exported_vars, assignments)
        elif script.endswith(".py"):
            self.run_python_script(key, script, parameters, exported_vars, assignments)
        else:
            self.run_script(key, script)

    def check_vault_not_present(self, key, script):
        script_path = os.path.join(os.getcwd(), "docker-share", script)

        with open(script_path) as f:
            contents = f.read()
        if "#{vault://" in contents:
            error_message = "Error running key %s - Script: %s. Error: " % (key, script)
            error_message += "Vault secret found inside script!. This is not allowed due to security reasons.\n"
            error_message += 'Use "parameters" in config.json instead.\n'
            error_message += 'i.e.: "parameters": {"param1": "#{vault://param1}"}'
            ACLogger.log_and_print_error(error_message)
            raise Exception(error_message)

    def run_jupyter_notebook(self, key, script, parameters, exported_vars, assignments):
        if JUPYTER_UNAVAILABLE:
            raise ImportError("Jupyter libraries not installed.")

        try:
            notebook_dir = os.path.join(os.getcwd(), "docker-share")
            notebook_path = os.path.join(notebook_dir, script)

            # Read jupyter notebook
            with open(notebook_path) as f:
                nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)

            # Generate unique python script name
            script_no_ext, _ = os.path.splitext(script)
            script_python = "{}_{}.py".format(script_no_ext, uuid4())
            script_python_path = os.path.join(notebook_dir, script_python)

            # Write jupyter notebook to python script
            with open(script_python_path, "w") as f:
                f.write(PythonExporter().from_notebook_node(nb)[0])
        except Exception as e:
            trace = traceback.format_exc()
            ACLogger.log_and_print_error("%s exception:\n%s" % (script, trace))
            value = {"trace": trace}

            # update progress with error coming from this key
            self.set_progress(key, value)
            raise e

        # Execute converted notebook
        self.run_python_script(key, script_python, parameters, exported_vars, assignments)

    def run_python_script(self, key, script, parameters, exported_vars, assignments):
        try:
            script_path = os.path.join(os.getcwd(), "docker-share", script)
            skip_globals = set(globals().keys())

            script_globals = {
                "LOGGER": ACLogger,
                "HELPERS": ACHelpers,
                "vault_resolve": ACHelpers.replace_vault_in_text,
                "vault_resolve_dict": ACHelpers.resolve_secrets,
            }
            script_globals.update(parameters)
            skip_globals.union(script_globals.keys())

            result = runpy.run_path(script_path, init_globals=script_globals, run_name="__main__")

            # export runtime variables
            for key, value in result.items():
                if key not in skip_globals and key in exported_vars:
                    self.set_progress(key, value)

            # map files to runtime variables
            for variable, mapping in assignments.items():
                if not os.path.isabs(mapping):
                    mapping = os.path.join(os.getcwd(), mapping)
                with open(mapping, "r") as f:
                    self.set_progress(variable, f.read())
        except SystemExit as e:
            exitcode = e.code
            error_msg = f"Script {script}: returned with exit code: {exitcode}"
            ACLogger.log_and_print(error_msg)
            value = {"trace": error_msg}
            self.set_progress(key, value)
            raise e
        except Exception as e:
            trace = traceback.format_exc()
            ACLogger.log_and_print_error("%s exception:\n%s" % (script, trace))
            value = {"trace": trace}

            # update progress with error coming from this key
            self.set_progress(key, value)
            raise e

    def run_script(self, key, script):
        # make sure we have permissions to execute the scripts
        for step in os.walk(os.getcwd() + "/docker-share"):
            path, files = step[0], step[2]
            for fi in files:
                os.chmod(path + "/" + fi, 0o777)
        # run the scripts
        try:
            command = ["./docker-share/" + script]
            output = subprocess.check_output(command, encoding="utf-8", stderr=subprocess.STDOUT)
            ACLogger.log_shell_output(output)
        except OSError as e:
            ACLogger.log_and_print_error(
                "Unable to execute %s. Check the name is correct and the file is there" % script
            )
            # update progress with error coming from this key
            self.set_progress(key, "error: %s" % str(e))
            raise e
        except subprocess.CalledProcessError as e:
            ACLogger.log_and_print_error(e.output)
            ACLogger.log_and_print_error("Process returned error code %s" % str(e.returncode))
            # update progress with error coming from this key
            self.set_progress(key, "error: %s" % str(e))
            raise e

    def determine_package_manager(self):
        with open("/etc/os-release", "r") as os_info_file:
            os_info = [x.strip() for x in os_info_file.readlines()]
        os_name = [x for x in os_info if x.startswith("ID=")][0]
        return "yum" if "amzn" in os_name else "apt"

    def install_pip_dependencies(self, dependencies, user=False):
        ACLogger.log_and_print("Installing runtime pip dependencies ...")
        if not dependencies or len(dependencies) == 0:
            ACLogger.log_and_print("Nothing to install")
            return

        # create requirements file
        requirements_file_data = "\n".join(dependencies)
        with open("runtime-requirements.txt", "w") as f:
            f.write(requirements_file_data)

        # install pip packages
        command = ["pip3", "install", "-r", "runtime-requirements.txt"]
        if user:
            command.insert(2, "--user")

        try:
            output = subprocess.check_output(command, encoding="utf-8", stderr=subprocess.STDOUT)
            prefix = "Pip Installation done"
            ACLogger.log_shell_output(output, prefix=prefix, print_lines=True)
            return
        except subprocess.CalledProcessError as e:
            ACLogger.log_and_print_error("Unable to install dependencies, error:\n%s" % e.output)
            raise e
        except Exception as e:
            ACLogger.log_and_print_error("Unable to install dependencies, Unknown error:\n%s" % traceback.format_exc())
            raise e

    def install_apt_dependencies(self, dependencies):
        ACLogger.log_and_print("Installing runtime apt dependencies ...")
        if not dependencies or len(dependencies) == 0:
            ACLogger.log_and_print("Nothing to install")
            return

        # install apt packages
        command = ["apt-get", "-y", "install"] + list(dependencies)
        try:
            output = subprocess.check_output(command, encoding="utf-8", stderr=subprocess.STDOUT)
            prefix = "Apt Installation done"
            ACLogger.log_shell_output(output, prefix=prefix, print_lines=True)
            return
        except subprocess.CalledProcessError as e:
            ACLogger.log_and_print_error("Unable to install apt dependencies, error:\n%s" % e.output)
            raise e
        except Exception as e:
            ACLogger.log_and_print_error(
                "Unable to install apt dependencies, Unknown error:\n%s" % traceback.format_exc()
            )
            raise e

    def install_yum_dependencies(self, dependencies):
        ACLogger.log_and_print("Installing runtime yum dependencies ...")
        if not dependencies or len(dependencies) == 0:
            ACLogger.log_and_print("Nothing to install")
            return

        # install yum packages
        command = ["sudo", "yum", "-y", "install"] + list(dependencies)
        try:
            output = subprocess.check_output(command, encoding="utf-8", stderr=subprocess.STDOUT)
            prefix = "Yum Installation done"
            ACLogger.log_shell_output(output, prefix=prefix, print_lines=True)
            return
        except subprocess.CalledProcessError as e:
            ACLogger.log_and_print_error("Unable to install yum dependencies, error:\n%s" % e.output)
            raise e
        except Exception as e:
            ACLogger.log_and_print_error(
                "Unable to install yum dependencies, Unknown error:\n%s" % traceback.format_exc()
            )
            raise e


if __name__ == "__main__":
    DKGeneralPurposeContainer().run()
