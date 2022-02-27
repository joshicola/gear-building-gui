import copy
import glob
import json
import os
import shutil
from collections import OrderedDict
from pathlib import Path

import pystache
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QWidget,
)

# TODO: This should be named "Gear Template Management"
"""
Provide the base run.py and utils package.
Creating build/validate/execute functional modules around specific command-line
programs.
Add a command-line "switch-detector" to populate the manifest config with values
to loop through.
Provide a library of code-blocks that facilitate certain functionality
module-based log reporting
bids functionality
verbose config validation against manifest
compress working directory to a file in output
notify on pep8 violations(??)
"""


class Script_Management:
    """
    Class for script management.
    """

    def __init__(self, main_window):
        """
        Initialize script management tab form elements with defaults. 

        Args:
            main_window (GearBuilderGUI):  The instantiated main window.
        """
        self.main_window = main_window
        self.ui = main_window.ui

        self.script_def = main_window.gear_def["script"]

        self.init_script_options()

        # Initialize script-template combo with available/valid script-templates
        self.init_script_templates()

        self.ui.cbo_script_template.currentIndexChanged.connect(
            self._update_script_options
        )

        self.ui.cbo_script_template.setCurrentIndex(0)
        self._update_script_options()

        self.ui.btn_Imp_Temp.clicked.connect(self.import_script_template)

    def import_script_template(self):
        """
        Import a script template from a local directory.
        """
        directory = str(
            QFileDialog.getExistingDirectory(
                self.main_window,
                (
                    "Select Folder to import gear template. "
                    "Must have .template directory"
                ),
            )
        )

        # Look for necessary directory and files
        template_dir = Path(directory) / ".template"
        if not template_dir.exists():
            raise Exception("Invalid template directory")

        gear_template_directives = template_dir / "gear_template_directives.json"
        if not gear_template_directives.exists():
            raise Exception("Missing gear_template_directives.json")
        template_directives = json.loads(gear_template_directives.read_text())

        # make it point to the template_dir
        template_directives["base_dir"] = str(template_dir)
        # save a copy of template directives in ~/.gearbuilder/gear_library/
        gear_library = Path(os.path.expanduser("~") + "/.gearbuilder/gear_library/")
        if not gear_library.exists():
            gear_library.mkdir(parents=True)
        gear_library_template_dir = gear_library / template_directives["template_name"]
        gear_library_template_dir.mkdir(parents=True, exist_ok=True)
        gear_library_template_dir /= "gear_template_directives.json"
        gear_library_template_dir.write_text(json.dumps(template_directives))
        self.init_script_templates()

    def init_script_templates(self):
        """
        Initialize script template combo from script_library sub-directories.

        Only valid templates are shown.
        """
        # TODO: Add directory to look in.  There should be a "user"-based configuration
        # directory to store the "full" path to a downloaded/cloned template.
        # This would allow refreshing the template from a source without having to dig
        # into the guts of the gearbuilder.

        # TODO: Load ~/.gearbuilder/gear_library/<template_name>/gear_template_directives.json
        #       get script directory from there.
        #       update from the <template_dir>/gear_template_directives.json in case
        #       the template has been updated.
        #       If the <template_dir>...cannot be found we must find or remove the template.
        default_script_templates = []
        script_dirs = glob.glob(str(self.main_window.root_dir / "script_library/*"))

        # check for imported gear templates
        gear_library = Path(os.path.expanduser("~") + "/.gearbuilder/gear_library/")
        if gear_library.exists():
            gear_library_script_dirs = glob.glob(str(gear_library / "*"))
            script_dirs.extend(gear_library_script_dirs)

        for script_dir in script_dirs:
            script_dir = Path(script_dir)
            if script_dir.is_dir():
                directive_path = script_dir / "gear_template_directives.json"
                if directive_path.exists():
                    template_directive = json.load(
                        open(directive_path, "r"), object_pairs_hook=OrderedDict,
                    )
                    # if this template is in the user gear library
                    if gear_library in script_dir.parents:
                        base_dir = Path(template_directive["base_dir"])
                        # if the origin of template exists
                        if base_dir.exists():
                            update_directive_path = (
                                base_dir / "gear_template_directives.json"
                            )
                            if update_directive_path.exists():
                                template_directive_update = json.load(
                                    open(update_directive_path, "r"),
                                    object_pairs_hook=OrderedDict,
                                )
                                template_directive.update(template_directive_update)
                                directive_path.write_text(
                                    json.dumps(template_directive)
                                )
                        else:
                            # if the origin of the template does not exist, remove it
                            shutil.rmtree(script_dir)
                            continue

                    # TODO: Add script-manifest validator....
                    default_script_templates.append(template_directive)

        self.ui.cbo_script_template.clear()
        # Set the script template data
        for template in default_script_templates:
            self.ui.cbo_script_template.addItem(
                template["template_description"], userData=template
            )

    def init_script_options(self):
        """
        Initialize script options ScrollArea
        """
        self.widget = QWidget()

        self.ui.fbox = QFormLayout()
        self.widget.setLayout(self.ui.fbox)

        # Scroll Area Properties
        self.ui.scrOptions.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.scrOptions.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.scrOptions.setWidgetResizable(True)
        self.ui.scrOptions.setWidget(self.widget)

    def _update_script_options(self):
        """
        Update subform script options on update of named script-template
        """
        # clear  QFormLayout()
        while self.ui.fbox.rowCount() > 0:
            self.ui.fbox.removeRow(0)

        # iterate through tags of current script_template
        data = self.ui.cbo_script_template.currentData()

        self.base_dir = Path(data["base_dir"])
        if (self.base_dir / ".template.gear.json").exists():
            self.main_window.gear_def.clear()
            with open(self.base_dir / ".template.gear.json", "r") as fp:
                self.main_window.gear_def.update(json.load(fp))
            self.main_window.menus.update_forms_from_gear_def()

        for k, v in data["tags"].items():
            Label = QLabel(k + ":")
            if isinstance(v, bool):
                object = QCheckBox()
                object.setChecked(v)
            else:
                object = QLineEdit()
                object.setText(v)
            object.setObjectName(k)
            self.ui.fbox.addRow(Label, object)

    def _update_form_from_script_def(self):
        """
        Select and populate the template-specific form values from the script_def.
        """
        for index in range(self.ui.cbo_script_template.count()):
            if (
                self.ui.cbo_script_template.itemData(index)["template_name"]
                == self.script_def["template_name"]
                and index != self.ui.cbo_script_template.currentIndex()
            ):
                self.ui.cbo_script_template.setCurrentIndex(index)
                self._update_script_options()
                break

        for i in range(self.ui.fbox.rowCount()):
            item = self.ui.fbox.itemAt(i * 2 + 1).widget()
            if isinstance(item, QLineEdit):
                if self.script_def.get(item.objectName()):
                    item.setText(self.script_def[item.objectName()])
            elif isinstance(item, QCheckBox):
                if self.script_def.get(item.objectName()):
                    item.setChecked(self.script_def[item.objectName()])

    def _update_script_def_from_form(self):
        """
        Clear and repopulate script_def from template-specific form values.
        """
        # unlike the manifest and dockerfile definitions, we need to clear the script
        # definition and repopulate.
        self.script_def.clear()

        script_def = {}

        data = self.ui.cbo_script_template.currentData()
        script_def["template_name"] = data["template_name"]
        for i in range(self.ui.fbox.rowCount()):
            item = self.ui.fbox.itemAt(i * 2 + 1).widget()
            if isinstance(item, QLineEdit):
                script_def[item.objectName()] = item.text()
            elif isinstance(item, QCheckBox):
                script_def[item.objectName()] = item.isChecked()

        self.script_def.update(script_def)

    def save(self, directory):
        """
        Saves the script hierarchy to provided directory.

        Args:
            directory (str): Path to output directory.
        """

        self._update_script_def_from_form()

        cbo_script_data = self.ui.cbo_script_template.currentData()

        for fl in cbo_script_data["templates"]:
            # Mustache Render
            script_template = (
                self.main_window.root_dir / cbo_script_data["base_dir"] / fl
            )

            if script_template.exists():
                output_filename = Path(directory) / fl.replace(".mu", "").replace(
                    ".mustache", ""
                )

                renderer = pystache.Renderer()

                template_output = renderer.render_path(
                    script_template, self.main_window.gear_def
                )

                # Ensure the path to write rendered template exists
                if not output_filename.parent.exists():
                    output_filename.parent.mkdir(parents=True)

                with open(output_filename, "w") as fp:
                    fp.write(template_output)
            else:
                # TODO: Alert user with PopUp
                # TODO: This should be considered an invalid script-template.
                print("template does not exist.")

        for fl in cbo_script_data["copy"]:
            source_path = self.main_window.root_dir / cbo_script_data["base_dir"] / fl
            destination_path = Path(directory) / fl
            if source_path.exists():
                if source_path.is_dir():
                    # shutil.copytree must have an empty destination
                    if destination_path.exists():
                        shutil.rmtree(destination_path)
                    shutil.copytree(source_path, destination_path)
                elif source_path.is_file():
                    shutil.copy(source_path, destination_path)
                else:
                    print("Unrecognized Path object.")

            else:
                # TODO: Alert user with PopUp... or cummulative errs in single popup
                print("File or path does not exist.")

    def _prep_gear_def(self, gear_def):
        """
        Give manifest some fields to assist in rendering the README.

        Args:
            gear_def (dict): Dictionary of manifest, docker, and other attributes.
        """
        local_manifest = gear_def["manifest"]
        # Check for non-zero number of inputs
        if len(local_manifest["inputs"].keys()) > 0:
            local_manifest["has_inputs"] = True

        local_manifest["inputs_list"] = []
        for inp, val in local_manifest["inputs"].items():
            val["name"] = inp
            local_manifest["inputs_list"].append(val)

        # Check for a non-zero number of configs
        if len(local_manifest["config"].keys()) > 0:
            local_manifest["has_configs"] = True

        local_manifest["config_list"] = []
        for conf, val in local_manifest["config"].items():
            val["name"] = conf
            if "default" in val.keys():
                val["default_val"] = {"val": val["default"]}
            local_manifest["config_list"].append(val)

        # Prep Dockerfile_def for rendering
        local_dockerfile = gear_def["dockerfile"]
        # Check for non-zero number of inputs
        if len(local_dockerfile["apt_get"]) > 0:
            local_dockerfile["has_apt"] = True

        # Check for a non-zero number of configs
        if len(local_dockerfile["pip"]) > 0:
            local_dockerfile["has_pip"] = True

        # Check for a non-zero number of configs
        if len(local_dockerfile["ENV"]) > 0:
            local_dockerfile["has_env"] = True

    def _render_templates(self, gear_def, gear_directives, output_dir):
        """
        Iterate through and render all file and folder templates in the gear.

        Args:
            gear_def (dict): Dictionary of manifest, docker, and other attributes.
            gear_directives (dict): Dictionary containing the templates to render.
            output_dir (Pathlike): Top level directory to write gear to.
        """
        renderer = pystache.Renderer()
        # Iterate through the templates and render them
        for template_file in gear_directives["templates"]:
            # there may be multiple templates for a template directive
            # this is where we initialize these flags
            template_files = None
            template_file_in, template_file_out = None, None
            # ":" is the delimiter between "source" and "destination"
            if ":" in template_file:
                template_file_in, template_file_out = template_file.split(":")
                # the "destination" may be a mustache template to render to
                # a specified path
                template_file_out = renderer.render(template_file_out, gear_def)

            # iterate through directories with wildcard
            if "*" in template_file:
                if not template_file_in:
                    template_file_in = template_file
                    template_file_out = template_file_in.replace("*", "")
                template_files = glob.glob(str(self.base_dir / template_file_in))

            # iterating through the wildcards
            if template_files:
                for template_fl in template_files:
                    with open(self.base_dir / template_fl, "r") as fp:
                        template = fp.read()
                    rendered_template = renderer.render(template, gear_def)
                    if template_file_out:
                        output_path = output_dir / template_file_out
                        output_fl = output_path / Path(template_fl).name
                    else:
                        output_fl = Path(output_dir) / template_fl

                    output_path.mkdir(parents=True, exist_ok=True)
                    with open(output_fl, "w") as fp:
                        fp.write(rendered_template)

            # or rendering the file-level template
            else:
                with open(self.base_dir / template_file, "r") as fp:
                    template = fp.read()
                rendered_template = renderer.render(template, gear_def)
                with open(output_dir / template_file.replace(".mu", ""), "w") as fp:
                    fp.write(rendered_template)

    def _copy_files(self, gear_directives, output_dir):
        """
        Copy files from the template to the gear.

        Args:
            gear_directives (dict): Dicitonary of files to copy.
            output_dir (Pathlike): Top level directory to write gear to.
        """
        for template_file in gear_directives["copy"]:
            template_file_path = self.base_dir / template_file
            if template_file_path.is_file():
                shutil.copy(template_file_path, output_dir)
            elif template_file_path.is_dir():
                shutil.copytree(
                    template_file_path,
                    output_dir / template_file_path.name,
                    dirs_exist_ok=True,
                )

    def render_and_copy_templates(self, directory):
        """
        Renders or copies all templates in the script-template directory.

        Args:
            directory (str): Path to output directory.
        """
        self.main_window.dockerfile._update_dockerfile_def_from_form()
        self._update_script_def_from_form()

        cbo_script_data = self.ui.cbo_script_template.currentData()
        if cbo_script_data["base_dir"].startswith("/"):
            self.base_dir = Path(cbo_script_data["base_dir"])
        else:
            self.base_dir = self.main_window.root_dir / cbo_script_data["base_dir"]
        gear_def = copy.deepcopy(self.main_window.gear_def)
        self._prep_gear_def(gear_def)
        self._render_templates(gear_def, cbo_script_data, Path(directory))
        self._copy_files(cbo_script_data, Path(directory))
        if "README.md.mu" not in cbo_script_data["templates"]:
            self.main_window.manifest.save_draft_readme(Path(directory))
        if "Dockerfile.mu" not in cbo_script_data["templates"]:
            self.main_window.dockerfile.save(Path(directory))

