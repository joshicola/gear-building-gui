#!/usr/bin/env python3
import os
import logging

from gear_toolkit import gear_toolkit_context
from gear_toolkit import command_line

log = logging.getLogger(__name__)


def main(context):
    # build and execute Parameters for {name}
    try:
        # build the command string
        command = ['{base_command}']

        # this gathers the configuration values ONLY
        # for including input values, see build_validate_execute
        for key in context.config.keys():
            command.append(context.config[key])

        # execute the command string
        command_line.exec_command(command)

    except Exception as e:
        log.exception(e,)
        log.fatal(
            'Error executing {name}.',
        )
        return 1

    log.info("{name} completed Successfully!")
    return 0


if __name__ == '__main__':
    with gear_toolkit_context.GearToolkitContext() as gear_context:
        gear_context.init_logging()
        exit_status = main(gear_context)

    log.info('exit_status is %s', exit_status)
    os.sys.exit(exit_status)
