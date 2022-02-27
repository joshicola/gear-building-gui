#!/usr/bin/env python3
import os
import os.path as op
import json
import subprocess as sp
import copy
import shutil

import flywheel
from utils import args
from utils.custom_logger import get_custom_logger, log_config
from utils import validate_config

if __name__ == '__main__':
    # Get the Gear Context
    context = flywheel.GearContext()
    # Activate custom logger
    context.log = get_custom_logger('[flywheel/hello-world]')

    # Validate gear configuration against gear manifest
    try:
        validate_config.validate_config_against_manifest(context)
    except Exception as e:
        context.log.fatal(e,)
        context.log.fatal(
            'Please make the prescribed corrections and try again.'
        )
        os.sys.exit(1)
    # Set up Custom Dicionary to host user variables
    context.custom_dict = {}

    # Instantiate Environment Variables
    # This will always be '/tmp/gear_environ.json' with these
    # environments defined in the Dockerfile and exported from there.
    with open('/tmp/gear_environ.json', 'r') as f:
        environ = json.load(f)

    context.custom_dict['environ'] = environ

    # Report on Inputs and configuration parameters to the log
    log_config(context)

    # Build, Validate, and execute Parameters Hello World
    try:
        args.build(context)
        args.validate(context)
        args.execute(context)

    except Exception as e:
        context.log.fatal(e,)
        context.log.fatal(
            'Error executing Hello World.',
        )
        os.sys.exit(1)

    context.log.info("Hello World completed Successfully!")
    os.sys.exit(0)
