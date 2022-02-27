# Dockerfile exported by GearBuilderGUI. Stash edits before export again

# Inheriting from established docker image:
FROM {{dockerfile.FROM}}

# Inheriting from established docker image:
LABEL maintainer="{{{dockerfile.Maintainer}}}"

{{#dockerfile.has_apt}}
# Install APT dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
{{/dockerfile.has_apt}}
{{#dockerfile.apt_get}}
    {{name}}{{#version}}={{/version}}{{version}} \
{{/dockerfile.apt_get}}
{{#dockerfile.has_apt}}
    && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
{{/dockerfile.has_apt}}

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
WORKDIR ${FLYWHEEL}

{{#dockerfile.has_pip}}
COPY requirements.txt ${FLYWHEEL}/

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

# Make directory for flywheel spec (v0):
ENV FLYWHEEL=/flywheel/v0
WORKDIR ${FLYWHEEL}
{{Something_about_copying_specific_files_and_folders.TBA}}
# Copy executable/manifest to Gear
COPY run.py ${FLYWHEEL}/run.py
COPY manifest.json ${FLYWHEEL}/manifest.json

# ENV preservation for Flywheel Engine
RUN python -c 'import os, json; f = open("/tmp/gear_environ.json", "w");json.dump(dict(os.environ), f)'

# Configure entrypoint
ENTRYPOINT ["/flywheel/v0/run.py"]