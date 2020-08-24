import json
import os
from pathlib import Path

import pystache
from PyQt5 import QtCore, QtGui, QtWidgets

from gear_builder_gui.config_dialog import config_dialog
from gear_builder_gui.input_dialog import input_dialog


class Manifest:
    """
    A class to manage the manifest of a gear

    TODO: Include the flywheel gear toolkit manifest class
    """

    def __init__(self, main_window):
        """
        Initialize manifest.

        Args:
            main_window (GearBuilderGUI): The instantiated main window.
        """
        self.main_window = main_window
        self.ui = main_window.ui

        # Initialize "input" Section
        self.ui.cmbo_inputs.currentIndexChanged.connect(self.update_tooltip)
        self.ui.btn_input_add.clicked.connect(self.add_input)
        self.ui.btn_input_edit.clicked.connect(self.edit_input)
        self.ui.btn_input_delete.clicked.connect(self.delete_input)
        # Initialize "config" Section
        self.ui.cmbo_config.currentIndexChanged.connect(self.update_tooltip)
        self.ui.btn_config_add.clicked.connect(self.add_config)
        self.ui.btn_config_edit.clicked.connect(self.edit_config)
        self.ui.btn_config_delete.clicked.connect(self.delete_config)
        # Disable edit/delete buttons on default:
        self.ui.btn_input_edit.setEnabled(False)
        self.ui.btn_input_delete.setEnabled(False)
        self.ui.btn_config_edit.setEnabled(False)
        self.ui.btn_config_delete.setEnabled(False)
        # Save/load functionality
        self.ui.btn_load_manifest.clicked.connect(self.load_manifest_from_file)
        self.ui.btn_save_manifest.clicked.connect(self.save_manifest)
        # connect to docker "maintainer" and validators
        self.ui.txt_maintainer.textChanged.connect(self.update_maintainers)
        self.init_validators()
        # initialize a manifest object
        self.manifest = main_window.gear_def["manifest"]

    def update_maintainers(self):
        """
        Coordinate the maintainer text across Dockerfile and manifest.
        """
        if self.ui.txt_maintainer.text() is not self.ui.txt_maintainer_2.text():
            self.ui.txt_maintainer_2.setText(self.ui.txt_maintainer.text())

    # Add functionality to the input add/edit/deleted buttons
    def add_input(self):
        """
        Add input to the input combo box through input dialog
        """
        dialog = input_dialog()
        name, data = dialog.get_data()
        if name is not None:
            self.ui.cmbo_inputs.addItem(name, userData=data)
            self.ui.btn_input_edit.setEnabled(True)
            self.ui.btn_input_delete.setEnabled(True)

    def edit_input(self):
        """
        Edit input through input dialog
        """
        obj = self.ui.cmbo_inputs
        name = obj.currentText()
        data = obj.currentData()
        dialog = input_dialog()
        name_upd, data = dialog.get_data(cbo_val=(name, data))
        if name_upd is not None:
            i = obj.findText(name)
            obj.setItemText(i, name_upd)
            obj.setItemData(i, data)

    def delete_input(self):
        """
        Delete selected input object from the input combo
        """
        i = self.ui.cmbo_inputs.currentIndex()
        self.ui.cmbo_inputs.removeItem(i)
        if self.ui.cmbo_inputs.count() == 0:
            self.ui.btn_input_edit.setEnabled(False)
            self.ui.btn_input_delete.setEnabled(False)

    def update_tooltip(self):
        """
        Update tooltip of config/input combo box item.
        """
        sender = self.main_window.sender()
        if "inputs" in sender.objectName():
            cbo_obj = self.ui.cmbo_inputs
        elif "config" in sender.objectName():
            cbo_obj = self.ui.cmbo_config
        else:
            cbo_obj = None

        if cbo_obj:
            cbo_name = cbo_obj.currentText()
            cbo_data = cbo_obj.currentData()
            tool_tip_text = ""
            for k, v in cbo_data.items():
                tool_tip_text += k + ": " + str(v) + "\n"
            cbo_obj.setToolTip(tool_tip_text)

    def add_config(self):
        """
        Add a config object to the config combo box through the config dialog.
        """
        dialog = config_dialog()
        name, data = dialog.get_data()
        if name is not None:
            self.ui.cmbo_config.addItem(name, userData=data)
            self.ui.btn_config_edit.setEnabled(True)
            self.ui.btn_config_delete.setEnabled(True)

    def edit_config(self):
        """
        Edit selected config object through the config dialog.
        """
        obj = self.ui.cmbo_config
        name = obj.currentText()
        data = obj.currentData()
        dialog = config_dialog()
        name_upd, data = dialog.get_data(cbo_val=(name, data))
        if name_upd is not None:
            i = obj.findText(name)
            obj.setItemText(i, name_upd)
            obj.setItemData(i, data)

    def delete_config(self):
        """
        Delete selected config object from the config combo
        """
        i = self.ui.cmbo_config.currentIndex()
        self.ui.cmbo_config.removeItem(i)
        if self.ui.cmbo_config.count() == 0:
            self.ui.btn_config_edit.setEnabled(False)
            self.ui.btn_config_delete.setEnabled(False)

    def _update_manifest_from_form(self):
        """
        Update the manifest dictionary from the contents of the manifest tab.

        This will perserve any items in the self.manifest dictionary not referenced by
        the form.

        TODO: I want to implement a _update_form_from_manifest function.
        """
        manifest = {}
        # Required keys all manifests have
        keys = [
            "name",
            "label",
            "description",
            "author",
            "maintainer",
            "license",
            "url",
            "source",
            "cite",
            "version",
        ]
        for key in keys:
            text_obj = eval("self.ui.txt_" + key)
            text_type = type(eval("self.ui.txt_" + key))
            if text_type == QtWidgets.QPlainTextEdit:
                text_value = text_obj.toPlainText()
            elif text_type == QtWidgets.QComboBox:
                text_value = text_obj.currentText()
            else:
                text_value = text_obj.text()
            manifest[key] = text_value

        # Build Custom section
        custom = {}
        custom["docker-image"] = (
            "flywheel/" + manifest["name"] + ":" + manifest["version"]
        )
        gear_builder = {}
        # gear category on radio button
        if self.ui.rdo_analysis.isChecked():
            gear_builder["category"] = "analysis"
        else:
            gear_builder["category"] = "converter"

        gear_builder["image"] = custom["docker-image"]

        custom["gear-builder"] = gear_builder
        # if "suite"
        if self.ui.chk_flywheel.isChecked():
            flywheel = {}
            flywheel["suite"] = self.ui.txt_suite.text()
            custom["flywheel"] = flywheel

        manifest["custom"] = custom

        # Build inputs section
        # Each input item consists of the text (key) of a combo box and
        # specifically constructed data (a dictionary).
        inputs = {}
        cbo_obj = self.ui.cmbo_inputs
        for i in range(cbo_obj.count()):
            inputs[cbo_obj.itemText(i)] = cbo_obj.itemData(i)

        manifest["inputs"] = inputs

        # Build config section
        # Each config item consists of the text (key) of a combo box and
        # specifically constructed data (a dictionary).
        config = {}
        cbo_obj = self.ui.cmbo_config
        for i in range(cbo_obj.count()):
            config[cbo_obj.itemText(i)] = cbo_obj.itemData(i)

        manifest["config"] = config
        # The command
        manifest["command"] = "/flywheel/v0/run.py"

        # Using an "update" here instead of a total replace preserves items that may
        # have been loaded.
        self.manifest.update(manifest)

    def load_manifest_from_file(self):
        """
        Load manifest from file.
        """
        manifest_file = QtWidgets.QFileDialog.getOpenFileName(
            self.main_window, "Select manifest.json to load.", filter="manifest.json"
        )

        # TODO: Should I warn about replacement of all manifest values?
        if len(manifest_file[0]) > 0:
            with open(manifest_file[0], "r") as manifest_raw:
                manifest = json.load(manifest_raw)

            self.manifest.clear()
            self.manifest.update(manifest)

            self._update_form_from_manifest()

    def _update_form_from_manifest(self):
        """
        Update form values from stored manifest.
        """
        # NOTE: This would be a good place to warn if the loaded manifest was invalid
        # Required manifest keys:
        keys = [
            "name",
            "label",
            "description",
            "author",
            "maintainer",
            "license",
            "url",
            "source",
            "cite",
            "version",
        ]
        try:
            for key in keys:
                text_obj = eval("self.ui.txt_" + key)
                text_type = type(eval("self.ui.txt_" + key))
                if self.manifest.get(key):
                    text_value = self.manifest[key]
                else:
                    text_value = ""
                if text_type == QtWidgets.QPlainTextEdit:
                    text_value = text_obj.setPlainText(text_value)
                elif text_type == QtWidgets.QComboBox:
                    index = text_obj.findText(text_value)
                    if index:
                        text_obj.setCurrentIndex(index)
                else:
                    text_obj.setText(text_value)
            # load custom fields
            custom = self.manifest["custom"]
            self.ui.rdo_analysis.setChecked(
                custom["gear-builder"]["category"] == "analysis"
            )
            if custom.get("flywheel"):
                self.ui.chk_flywheel.setChecked(True)
                self.ui.txt_suite.setText(custom["flywheel"]["suite"])

            # load inputs section
            inputs = self.manifest["inputs"]

            cbo_obj = self.ui.cmbo_inputs
            cbo_obj.clear()
            for name, data in inputs.items():
                cbo_obj.addItem(name, userData=data)

            if cbo_obj.count() > 0:
                self.ui.btn_input_edit.setEnabled(True)
                self.ui.btn_input_delete.setEnabled(True)

            # load configs section
            config = self.manifest["config"]

            cbo_obj = self.ui.cmbo_config
            cbo_obj.clear()
            for name, data in config.items():
                cbo_obj.addItem(name, userData=data)

            if cbo_obj.count() > 0:
                self.ui.btn_config_edit.setEnabled(True)
                self.ui.btn_config_delete.setEnabled(True)

        except Exception as e:
            print(e)

    def save_manifest(self):
        """
        Select destination to save manifest.json file.
        """
        directory = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self.main_window, "Select Folder to save manifest.json."
            )
        )
        if len(directory) > 0:
            self.save(directory)

    def save(self, directory):
        """
        Save self.manifest dictionary to manifest.json file in the indicated directory.

        Args:
            directory (str): Path to directory.
        """
        directory = Path(directory)
        self._update_manifest_from_form()

        json.dump(self.manifest, open(directory / "manifest.json", "w"), indent=2)

    def save_draft_readme(self, directory, readme_template=None):
        """
        Saves draft of README.md to indicated directory.

        Args:
            directory (str): Path to directory.
            readme_template (str, optional): Path to the mustache template to use.
                Defaults to None.

        """
        directory = Path(directory)
        if not readme_template:
            source_dir = self.main_window.root_dir / "default_templates"
            readme_template = source_dir / "README.md.mu"
        renderer = pystache.Renderer()

        # Check for non-zero number of inputs
        if len(self.manifest["inputs"].keys()) > 0:
            self.manifest["has_inputs"] = True

        self.manifest["inputs_list"] = []
        for inp, val in self.manifest["inputs"].items():
            val["name"] = inp
            self.manifest["inputs_list"].append(val)

        # Check for a non-zero number of configs
        if len(self.manifest["config"].keys()) > 0:
            self.manifest["has_configs"] = True

        self.manifest["config_list"] = []
        for conf, val in self.manifest["config"].items():
            val["name"] = conf
            if "default" in val.keys():
                val["default_val"] = {"val": val["default"]}
            self.manifest["config_list"].append(val)

        template_output = renderer.render_path(
            readme_template, {"manifest": self.manifest}
        )

        with open(directory / "README.md", "w") as fp:
            fp.write(template_output)

    def _check_description_text_length(self):
        """
        Constrains the length of the QPlainTextEdit txt_description member.

        The maxLength is initialized below from the manifest schema. The QPlainTextEdit
        object does not have an automatic length constraint.
        """
        obj = self.ui.txt_description
        if len(obj.toPlainText()) > obj.maxLength:
            obj.textCursor().deletePreviousChar()

    def init_validators(self):
        """
        Initializes the field validators to the manifest schema.

        TODO: Use a local copy of the manifest schema instead of downloading.
        """
        # spec_url = (
        #    "https://gitlab.com/flywheel-io/public/"
        #    "gears/-/raw/master/spec/manifest.schema.json"
        # )
        # request = requests.get(spec_url)
        # url = urllib.request.urlopen(spec_url)
        with open(
            self.main_window.root_dir
            / "gear_builder_gui/resources/manifest.schema.json",
            "r",
        ) as fp:
            gear_spec = json.load(fp)

        keys = [
            "name",
            "label",
            "description",
            "author",
            "maintainer",
            "license",
            "url",
            "source",
            "cite",
            "version",
        ]
        for key in keys:
            gear_spec_item = gear_spec["properties"][key]
            if key == "license":
                text_obj = self.ui.txt_license
                text_obj.addItems(gear_spec["properties"]["license"]["enum"])
                text_obj.setCurrentIndex(text_obj.__len__() - 1)
            else:
                text_obj = eval("self.ui.txt_" + key)
                text_type = type(eval("self.ui.txt_" + key))
                if "maxLength" in gear_spec_item.keys():
                    text_obj.maxLength = gear_spec_item["maxLength"]

                if "pattern" in gear_spec_item.keys():
                    rx = QtCore.QRegExp(gear_spec_item["pattern"])
                    val = QtGui.QRegExpValidator(rx, self.main_window)
                    text_obj.setValidator(val)
                elif key == "version":
                    rx = QtCore.QRegExp(
                        "^((([0-9]+)\\.([0-9]+)\\.([0-9]+)"
                        "(?:-_([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?)"
                        "(?:\\+([0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?)$"
                    )
                    val = QtGui.QRegExpValidator(rx, self.main_window)
                    text_obj.setValidator(val)

                if text_type == QtWidgets.QPlainTextEdit:
                    text_obj.textChanged.connect(self._check_description_text_length)

            if "description" in gear_spec_item.keys():
                text_obj.whatsThis = gear_spec_item["description"]
                text_obj.setToolTip(gear_spec_item["description"])
