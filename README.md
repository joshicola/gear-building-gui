# gear-building-gui
PyQt5 forms and functionality to ease the pain of the gear building experience.
It is currently a prototype that writes the manifest.json variables and input
specifications.  See notes below for proposed functionality.

PyQt5 is a platform-independent gui framework. Build on any deploy on every. Installation is possible through both conda and pip.

Would it be possible to package in a pip-installable repository?

The manifest portion of the gear-building-gui is developed as the prototype.
It currently:

* provides edit functionality for gear name, label, description, author, maintainer,
source, url, cite, and version
* automatically populates the "custom" section with the docker file names
* provides add, edit, delete functionality of input elements.
* provides add, edit, delete functionality of config elements.
* saves to a 'manifest.json' file

![Crude Ugly Prototype](Screenshot.png "Crude and Ugly Prototype of gear-builder-gui")

## Proposed Functionality

This is a prototype and a work-in-progress that will take time and concerted effort
to make ready for public release. Below are some of the proposed functionality
for future development.  It is envisioned that the following sections will have
their own "tab" in the PyQt gui.

### Manifest

Although the manifest portion is the most developed, it requires some additional functionality to make it truly useful:

* load and parse existing manifest.json file
* load and display options from gear specification where required
* validate entries with respects to the gear specification

### Dockerfile

We want to be able to view, edit, and validate dependecies for our gear image.

* add, edit, delete dockerfile blocks that automate apt-get installations, pip dependencies, and clean-up after those blocks.  More downloaded application-specific blocks should be edited by hand.
* listing of flywheel-provided base images with add, edit, delete (not flywheel) functionality.

### Runscript prototyping

The main purpose of the "runscript prototyping" is to give the user a self-documenting script/package/module framework to build their gears within...giving them support to automatically employ best practices while simultaneously providing the rational (developer-provided comments around code-blocks).

* Provide the base run.py and utils package.
* Creating build/validate/execute functional modules around specific command-line programs.  
* Add a command-line "switch-detector" to populate the manifest config with values to loop through.
* Provide a library of code-blocks that facilitate certain functionality
    - module-based log reporting
    - bids functionality
    - verbose config validation against manifest
    - compress working directory to a file in output
* notify on pep8 violations(??)
