#!/usr/bin/env python3
import logging
import os

from flywheel_gear_toolkit import GearToolkitContext
from flywheel_gear_toolkit.interfaces import command_line

log = logging.getLogger(__name__)


def main(context):
    # build and execute Parameters for {{manifest.name}}
    try:
        # build the command string
        command = ["{{script.base_command}}"]
        # This block of code is active when not rendered by pystache
        # {{#if_not_mustache_rendered}}
        command = ["echo"]
        # {{/if_not_mustache_rendered}}
        # this gathers the configuration values ONLY and uses them as positional
        # arguments to "{{script.base_command}}"
        # for including input values, see build_validate_execute
        for key in context.config.keys():
            command.append(context.config[key])

        # execute the command string
        command_line.exec_command(command)

    except Exception as e:
        log.exception(e,)
        log.fatal("Error executing {{manifest.name}}.",)
        return 1

    log.info("{{manifest.name}} completed Successfully!")
    return 0


if __name__ == "__main__":
    with GearToolkitContext() as gear_context:
        gear_context.init_logging()
        exit_status = main(gear_context)

    log.info("exit_status is %s", exit_status)
    os.sys.exit(exit_status)
