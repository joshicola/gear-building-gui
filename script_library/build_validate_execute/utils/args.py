import os.path as op
import sys
from collections import OrderedDict

from gear_toolkit.command_line import build_command_list, exec_command
import flywheel


def build(context):
    # use Ordered Dictionary to keep the order created.
    # Default in Python 3.6 onward
    params = OrderedDict()
    config = context.config
    inputs = context._inputs

    # Default behavior here is to have gear-configuration parameters
    # that are the same as the command-line parameters
    # e.g. --<name>=<value>
    for key in config.keys():
        params[key] = config[key]

    # inputs (file inputs) have a path
    # e.g. --<name>=<input file path>
    for key in inputs.keys():
        params[key] = context.get_input_path(key)

    return params


def validate(params):
    """
    validate the given parameters against potential conflicts

    Some command parameters can be mutually exclusive, that is, they cannot
    both be set to particular values and guarantee an error-free execution.

    This will be custom to each command and is initialized to `pass` for ease
    of representation.

    Args:
        params (dict): dictionary of pydeface parameters

    Raises:
        Exception: if we have parameter conflicts, we raise an exception and
            conclude our execution instead of attempting a command execution
            that is guaranteed to fail.
    """

    pass


def execute(context, params, dry_run=False, environ=None):
    # Get Params
    command = ['{base_command}']

    # Build command-line parameters
    command = build_command_list(command, params)

    # Extend with positional arguments
    # command.append(context.get_input_path('infile'))

    exec_command(command, environ=environ)
