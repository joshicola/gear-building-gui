FROM {{dockerfile.FROM}} as base

# Inheriting from established docker image:
LABEL maintainer="{{{dockerfile.Maintainer}}}"
{{#dockerfile.has_apt}}
# Install APT dependencies
RUN apt-get update && \
    curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get install -y --no-install-recommends \
{{/dockerfile.has_apt}}
{{#dockerfile.apt_get}}
    {{name}}{{#version}}={{/version}}{{version}} \
{{/dockerfile.apt_get}}
{{#dockerfile.has_apt}}
    && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
{{/dockerfile.has_apt}}
# The last line above is to help keep the docker image smaller

RUN npm install -g bids-validator@1.5.4

{{#dockerfile.has_pip}}
# Install PIP Dependencies
RUN pip3 install --upgrade pip && \ 
    pip install -r requirements.txt && \
    rm -rf /root/.cache/pip
{{/dockerfile.has_pip}}

{{#dockerfile.has_env}}
# Specify ENV Variables
ENV \ 
{{/dockerfile.has_env}}
{{#dockerfile.ENV}}
    {{name}}={{value}} \
{{/dockerfile.ENV}}
*

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
WORKDIR ${FLYWHEEL}

# Save docker environ
RUN python -c 'import os, json; f = open("/tmp/gear_environ.json", "w"); json.dump(dict(os.environ), f)' 

# Copy executable/manifest to Gear
COPY manifest.json ${FLYWHEEL}/manifest.json
COPY utils ${FLYWHEEL}/utils
COPY run.py ${FLYWHEEL}/run.py

# Configure entrypoint
RUN chmod a+x ${FLYWHEEL}/run.py
ENTRYPOINT ["/flywheel/v0/run.py"]
