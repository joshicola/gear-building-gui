import glob
import json
import shutil
from collections import OrderedDict
from pathlib import Path

import pystache
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QFormLayout, QLabel, QLineEdit, QWidget


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

    def init_script_templates(self):
        """
        Initialize script template combo from script_library sub-directories.

        Only valid templates are shown.
        """
        default_script_templates = []
        script_dirs = glob.glob(str(self.main_window.root_dir / "script_library/*"))
        for script_dir in script_dirs:
            script_dir = Path(script_dir)
            if script_dir.is_dir():
                manifest_path = script_dir / "script_manifest.json"
                if manifest_path.exists():
                    script_manifest = json.load(
                        open(manifest_path, "r"), object_pairs_hook=OrderedDict,
                    )
                    # TODO: Add script-manifest validator....
                    default_script_templates.append(script_manifest)

        # Set the script template data
        for template in default_script_templates:
            self.ui.cbo_script_template.addItem(
                template["template_name"], userData=template
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
        template_name = self.script_def["template_name"]
        index = self.ui.cbo_script_template.findText(template_name, Qt.MatchFixedString)
        if index >= 0:
            self.ui.cbo_script_template.setCurrentIndex(index)
            self._update_script_options()

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
