# gear-building-gui

This project provides a cross-platform graphical user interface to ease the pain and complexity of the gear-building experience.  It delivers a completely functional set of essential gear components for the user to customize.  This functional prototype delivers the following Minimum Viable Product to provide utility, ease of use, and adoption:

* Write of a complete manifest.json file
* Write a minimal, yet fully functional, Dockerfile
    - With appropriately asigned apt and pip packages
    - Asigning environment variables
* Write a minimal, yet fully functional, script/package/module structure
    - Manually customize for specific application

![Crude Ugly Prototype](Screenshot.png "Crude and Ugly Prototype of gear-builder-gui")

See notes below for current and proposed functionality.

This project is build in PyQt5, a platform-independent gui framework. Build on any deploy on every. The PyQt5 framework is available through both both conda and pip installers.

## Current Functionality

### Manifest

The manifest portion of the gear-building-gui is the most developed.
It currently:

* provides edit functionality for gear name, label, description, author, maintainer,
source, url, cite, and version
* automatically populates the "custom" section with the docker file names
* provides add, edit, delete functionality of input elements.
* provides add, edit, delete functionality of config elements.
* validates entries with respects to the gear specification
* saves to a 'manifest.json' file

### Dockerfile

A fully functional Dockerfile is provided as a template to work from.  Knowledge of docker commands is assumed.

* Provides interface to specify apt-get packages to install in Dockerfile
* Provides interface to specify pip packages to install in Dockerfile
* Provides interface to specify multiple environment values in Dockerfile
* Cross-references values with Manifest section to ensure consistency

### Gear script and modules

A fully functional "Hello World" Python gear script and utils package is provided as a template to work from. Familiarity with flywheel Python SDK is assumed.

## Proposed Functionality

This is a prototype and a work-in-progress that will take time and concerted effort
to make ready for public release. Below are some of the proposed functionality
for future development.  The following sections have
their own "tab" in the PyQt gui.

### Manifest Editing

Although the manifest portion is the most developed, it requires some additional functionality to make it truly useful:

* Need to add max/min vals and array size
* load and parse existing manifest.json file

### Dockerfile Editing

We want to be able to view, edit, and validate dependecies for our gear image.

* listing of flywheel-provided base images with add, edit, delete (not flywheel) functionality.

### Runscript prototyping

The main purpose of the "runscript prototyping" is to give the user a self-documenting script/package/module framework to build their gears within...giving them support to automatically employ best practices while simultaneously providing the rationale (developer-provided comments around code-blocks).

* Provide the base run.py and utils package.
* Creating build/validate/execute functional modules around specific command-line programs.  
* Add a command-line "switch-detector" to populate the manifest config with values to loop through.
* Provide a library of code-blocks that facilitate certain functionality
    - module-based log reporting
    - bids functionality
    - verbose config validation against manifest
    - compress working directory to a file in output
* notify on pep8 violations(??)
* integration with gear-toolkit

### Other

Other "Nice to Haves":

* create a pip-installable and conda-installable packages of the gear-builder-gui for ease of use and version management.
* Save a "Project" file that can be used as a template to add or remove desired features.
    - a json format having manifest, dockerfile, runscript sections (.gear???).
* Bundle all gear-essentials into a compressed file
    - manifest/dockerfile/runscripts/gear_definition (.gear???)