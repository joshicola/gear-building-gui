# Minimal Dockerfile for Hello-World Gear

# Use Ubuntu 16.04 LTS
FROM ubuntu:xenial

LABEL MAINTAINER="Flywheel <support@flywheel.io>"

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
WORKDIR ${FLYWHEEL}

# Copy executable/manifest to Gear
COPY run.py ${FLYWHEEL}/run.py
COPY utils ${FLYWHEEL}/utils
COPY manifest.json ${FLYWHEEL}/manifest.json

# ENV preservation for Flywheel Engine
RUN python -c 'import os, json; f = open("/tmp/gear_environ.json", "w"); json.dump(dict(os.environ), f)'

# Configure entrypoint
ENTRYPOINT ["/flywheel/v0/run.py"]
