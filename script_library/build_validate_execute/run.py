#!/usr/bin/env python3
import json
import logging
import os

from gear_toolkit import gear_toolkit_context
from utils import args

log = logging.getLogger(__name__)


def main(context):
    context.log_config()
    with open("/tmp/gear_environ.json", "r") as f:
        environ = json.load(f)

    # Build, Validate, and execute Parameters for {name}
    try:
        # build the command string
        params = args.build(context)
        args.validate(params)
        command = ["{{base_command}}"]
        args.execute(command, params, environ=environ)

    except Exception as e:
        context.log.fatal(e,)
        context.log.fatal("Error executing {{manifest.name}}.")
        return 1

    context.log.info("{{manifest.name}} completed Successfully!")
    return 0


if __name__ == "__main__":
    with gear_toolkit_context.GearToolkitContext() as gear_context:
        gear_context.init_logging()
        exit_status = main(gear_context)

    log.info("exit_status is %s", exit_status)
    os.sys.exit(exit_status)
