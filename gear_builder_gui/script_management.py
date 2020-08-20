"""
TODO: Very rudimentary at the moment. Would like to introduce
elements to both create and interpret mustache tags (e.g. {{keyword}}) with the
    following
intentions:
tags: replace these with txt/keyword/config_value or nothing/comments
      --this could be added to with a cbo_box that selects config key/value
        specifications
      --call it 'config_vals:'?
snippets: replace these with specified chunks of code or nothing/comments
run_code: replace these with the output of code run on manifest or nothing/comments

The above is fleshing out to be:
Stand-alone fill-in text is to be expressed as: {{script.<text_name>}}

Whole blocks of text will be expressed as:
{{#script.<block_name>}}
    print("Hi, I am a block of code")
{{/script.<block_name>}}
"""

import json
import os
import os.path as op
import shutil
from collections import OrderedDict
from pathlib import Path

import pystache
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QFormLayout, QLabel, QLineEdit, QWidget

# TODO: embed these templates within the sub-directories of "script_library"
#       Render only if they are valid.

default_script_templates = [
    {
        "template_name": "Simple Script",
        "base_dir": "script_library/simple_script/",
        "tags": {"base_command": "echo"},
        "templates": ["run.py"],
        "copy": [],
    },
    {
        "template_name": "Bids App Template",
        "base_dir": "script_library/bids-app-template/",
        "tags": OrderedDict(
            {
                "bids_command": "echo",
                "participant": "Subject 1",
                "cpus": False,
                "memory_available": False,
                "verbose": False,
                "needs_freesurfer_license": False,
                "bids_tree": False,
                "zip_htmls": False,
                "save_intermediate_output": False,
            }
        ),
        "templates": ["run.py"],
        "copy": ["utils", "LICENSE"],
    },
]


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

        # Set the script template data
        for template in default_script_templates:
            self.ui.cbo_script_template.addItem(
                template["template_name"], userData=template
            )

        self.ui.cbo_script_template.currentIndexChanged.connect(
            self._update_script_options
        )

        self.ui.cbo_script_template.setCurrentIndex(0)
        self._update_script_options()

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

    def _script_def_to_form(self):
        """
        Select and populate the template-specific form values from the script_def.
        """
        pass

    def _form_to_script_def(self):
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
                script_def[item.objectName()] = bool(item.checkState())

        self.script_def.update(script_def)

    def save(self, directory):
        """
        Saves the script hierarchy to provided directory.

        Args:
            directory (str): Path to output directory.
        """

        self._form_to_script_def()

        source_dir = Path(op.join(os.path.dirname(os.path.realpath(__file__)), ".."))
        cbo_script_data = self.ui.cbo_script_template.currentData()

        for fl in cbo_script_data["templates"]:
            # Mustache Render
            script_template = source_dir / cbo_script_data["base_dir"] / fl
            if script_template.exists():
                output_filename = Path(directory) / fl

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
                print("template does not exist.")

        for fl in cbo_script_data["copy"]:
            source_path = source_dir / cbo_script_data["base_dir"] / fl
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
