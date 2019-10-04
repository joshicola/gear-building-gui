# gear-building-gui

This project provides a cross-platform graphical user interface to ease the pain and complexity of the gear-building experience.  It delivers a completely functional set of essential gear components for the user to customize.  Although a functional prototype (see below),  extending to the following MVP would increase its utility, ease of use, and adoption:

* Read/Write/Validation of a complete manifest.json file
* Write a minimal, yet fully functional, Dockerfile
    - Manually specify dependencies
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
    - maximum/minimum value bounds not provided in gui
    - maximum/minimum array size not provided in gui
* saves to a 'manifest.json' file

### Dockerfile

A fully functional Dockerfile is provided as a template to work from.  Knowledge of docker commands is assumed.

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
* load and display options from gear specification where required
* validate entries with respects to the gear specification

### Dockerfile Editing

We want to be able to view, edit, and validate dependecies for our gear image.

* add, edit, delete dockerfile blocks that automate apt-get installations, pip dependencies, and clean-up after those blocks.  More downloaded application-specific blocks should be edited by hand.
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

### Other

Other "Nice to Haves":

* create a pip-installable and conda-installable packages of the gear-builder-gui for ease of use and version management.
