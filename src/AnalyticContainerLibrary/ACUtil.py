from .ACSingletons import ACLogger, ACHelpers
"""
The default logger, as a replacement of LOGGER injected
via globals on GPC.
"""
LOGGER = ACLogger


def get_parameter(name, default=None):
    """
    IDE-friendly option for retrieving parameters passed through container node.
    :param name: name of the parameter
    :param default: default value
    :return: the value of the parameter if exists, otherwise None or default.
    """
    return globals().get(name, default)


def export(name, value):
    """
    Exports a variable to be later picked from container node.
    :param name: name of the variable
    :param value: value
    :return: None
    """
    globals()[name] = value


def resolve_secret(name):
    """
    Replacement for globals version of secret resolve function.
    :param name:
    :return:
    """
    return ACHelpers.replace_vault_in_text(name)
