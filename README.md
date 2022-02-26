# fw-gear-building-gui

This is a graphical user interface (GUI) for building the essential components for flywheel ([*](#disclosure)) "gears" (dockerized algorithms for processing life-science data). 

Written in PyQt, this cross-platform graphical user interface eases the pain and complexity of the gear-building experience.  It delivers a completely functional set of essential gear components for the user to customize.  This functional prototype delivers the following:

* Write of a complete manifest.json file
* Write a draft of the gear's README.md file
    - With details filled in from the manifest.
* Write a minimal, yet fully functional, Dockerfile
    - With appropriately asigned apt and pip packages
    - Assigning environment variables
* Write a minimal, yet fully functional, script/package/module structure
    - Manually customize for specific application

![Crude Ugly Prototype](Screenshot.png "Crude and Ugly Prototype of gear-builder-gui")

See notes below for current and proposed functionality.

This project is build in PyQt5, a platform-independent gui framework. Build on any operating system, deploy on every operating system. The PyQt5 framework is available through both both conda and pip installers.



## Current Functionality

### Manifest

The manifest portion of the gear-building-gui is the most developed.
It currently:

* provides edit functionality for gear name, label, description, author, maintainer, source, url, cite, and version.
* automatically populates the "custom" section with the docker file names.
* provides add, edit, delete functionality of input elements.
* provides add, edit, delete functionality of config elements.
* validates entries with respects to the gear specification.
* loads existing `manifest.json` file to populate form.
* saves to a `manifest.json` file.
* saves a draft of a `README.md` file that is populated with values from the manifest.

### Dockerfile

A fully functional Dockerfile is provided as a template to work from.  Knowledge of docker commands is assumed.

* Provides interface to specify apt-get packages to install in Dockerfile.
* Provides interface to specify pip packages to install in Dockerfile.
* Provides interface to specify multiple environment values in Dockerfile.
* Cross-references 'maintainer' value with Manifest section to ensure consistency.

### Gear script and modules

A fully functional "Hello World" Python gear script and utils package is provided as a template to work from. Familiarity with flywheel Python SDK is assumed.

## Disclosure
This is a project that has been established and published by me, Joshua Jacobs, independent of Flywheel and its associates. This code is a contribution to the open source community on an "as-is" basis. Any questions about preferred "gear building" strategies should be directed at the representatives of Flywheel.

I have thoroughly enjoyed the process of architecting, designing, and building this project over time. Collaborations are welcomed.