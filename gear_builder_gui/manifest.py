import json
import os
import os.path as op
import urllib.request

import pystache
import requests
from PyQt5 import QtCore, QtGui, QtWidgets

from gear_builder_gui.config_dialog import config_dialog
from gear_builder_gui.input_dialog import input_dialog


class Manifest:
    """
     [summary]
    """

    def __init__(self, main_window):
        """
        __init__ [summary]

        Args:
            main_window ([type]): [description]
        """
        self.main_window = main_window
        self.ui = main_window.ui
        # Initialize "input" Section
        self.ui.btn_input_add.clicked.connect(self.add_input)
        self.ui.btn_input_edit.clicked.connect(self.edit_input)
        self.ui.btn_input_delete.clicked.connect(self.delete_input)
        # Initialize "config" Section
        self.ui.btn_config_add.clicked.connect(self.add_config)
        self.ui.btn_config_edit.clicked.connect(self.edit_config)
        self.ui.btn_config_delete.clicked.connect(self.delete_config)
        # Disable edit/delete buttons on default:
        self.ui.btn_input_edit.setEnabled(False)
        self.ui.btn_input_delete.setEnabled(False)
        self.ui.btn_config_edit.setEnabled(False)
        self.ui.btn_config_delete.setEnabled(False)
        # Save/load functionality
        self.ui.btn_load_manifest.clicked.connect(self.load_manifest)
        self.ui.btn_save_manifest.clicked.connect(self.save_manifest)
        # connect to docker "maintainer" and validators
        self.ui.txt_maintainer.textChanged.connect(self.update_maintainers)
        self.init_validators()
        # initialize a manifest object
        self.manifest = {}

    def update_maintainers(self):
        """
        update_maintainers [summary]
        """
        if self.ui.txt_maintainer.text() is not self.ui.txt_maintainer_2.text():
            self.ui.txt_maintainer_2.setText(self.ui.txt_maintainer.text())

    # Add functionality to the input add/edit/deleted buttons
    def add_input(self):
        """
        add_input [summary]
        """
        dialog = input_dialog()
        name, data = dialog.get_data()
        if name is not None:
            self.ui.cmbo_inputs.addItem(name, userData=data)
            self.ui.btn_input_edit.setEnabled(True)
            self.ui.btn_input_delete.setEnabled(True)

    def edit_input(self):
        """
        edit_input [summary]
        """
        obj = self.ui.cmbo_inputs
        name = obj.currentText()
        data = obj.currentData()
        dialog = input_dialog()
        name_upd, data = dialog.get_data(cbo_val=[name, data])
        if name_upd is not None:
            i = obj.findText(name)
            obj.setItemText(i, name_upd)
            obj.setItemData(i, data)

    def delete_input(self):
        """
        delete_input [summary]
        """
        i = self.ui.cmbo_inputs.currentIndex()
        self.ui.cmbo_inputs.removeItem(i)
        if self.ui.cmbo_inputs.count() == 0:
            self.ui.btn_input_edit.setEnabled(False)
            self.ui.btn_input_delete.setEnabled(False)

    def add_config(self):
        """
        add_config [summary]
        """
        dialog = config_dialog()
        name, data = dialog.get_data()
        if name is not None:
            self.ui.cmbo_config.addItem(name, userData=data)
            self.ui.btn_config_edit.setEnabled(True)
            self.ui.btn_config_delete.setEnabled(True)

    def edit_config(self):
        """
        edit_config [summary]
        """
        obj = self.ui.cmbo_config
        name = obj.currentText()
        data = obj.currentData()
        dialog = config_dialog()
        name_upd, data = dialog.get_data(cbo_val=[name, data])
        if name_upd is not None:
            i = obj.findText(name)
            obj.setItemText(i, name_upd)
            obj.setItemData(i, data)

    def delete_config(self):
        """
        delete_config [summary]
        """
        i = self.ui.cmbo_config.currentIndex()
        self.ui.cmbo_config.removeItem(i)
        if self.ui.cmbo_config.count() == 0:
            self.ui.btn_config_edit.setEnabled(False)
            self.ui.btn_config_delete.setEnabled(False)

    def _update_manifest_from_form(self):
        """
        _update_manifest_from_form [summary]
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

        self.manifest.update(manifest)

    def load_manifest(self):
        """
        load_manifest [summary]
        """
        manifest_file = QtWidgets.QFileDialog.getOpenFileName(
            self.main_window, "Select manifest.json to load.", filter="manifest.json"
        )

        # TODO: Should I warn about replacement of all manifest values?
        if len(manifest_file[0]) > 0:
            self.load_manifest_file(manifest_file[0])

    def load_manifest_file(self, manifest_file):
        """
        load_manifest_file [summary]

        Args:
            manifest_file ([type]): [description]
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
            self.manifest = json.load(open(manifest_file, "r"))
            for key in keys:
                text_obj = eval("self.ui.txt_" + key)
                text_type = type(eval("self.ui.txt_" + key))
                text_value = self.manifest[key]
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

            # load configs section
            config = self.manifest["config"]

            cbo_obj = self.ui.cmbo_config
            cbo_obj.clear()
            for name, data in config.items():
                cbo_obj.addItem(name, userData=data)

        except Exception as e:
            print(e)

    def save_manifest(self):
        """
        save_manifest [summary]
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
        save [summary]

        Args:
            directory ([type]): [description]
        """
        self._update_manifest_from_form()

        json.dump(
            self.manifest, open(op.join(directory, "manifest.json"), "w"), indent=2
        )

    def save_draft_readme(self, directory, readme_template=None):
        """
        save_draft_readme [summary]

        Args:
            directory ([type]): [description]
            readme_template ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        if not readme_template:
            source_dir = op.join(
                os.path.dirname(os.path.realpath(__file__)), "..", "default_templates"
            )
            readme_template = op.join(source_dir, "README.md.mu")
        renderer = pystache.Renderer()

        output = readme_template.replace(".mu", "")

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

        with open(op.join(directory, "README.md"), "w") as fp:
            fp.write(template_output)

        return 0

    def checkText(self):
        """
        checkText [summary]
        """
        obj = self.ui.txt_description
        if len(obj.toPlainText()) > obj.maxLength:
            obj.textCursor().deletePreviousChar()

    def init_validators(self):
        """
        init_validators [summary]
        """
        spec_url = (
            "https://gitlab.com/flywheel-io/public/"
            "gears/-/raw/master/spec/manifest.schema.json"
        )
        request = requests.get(spec_url)
        # url = urllib.request.urlopen(spec_url)
        gear_spec = json.loads(request.content)
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
                    text_obj.textChanged.connect(self.checkText)

            if "description" in gear_spec_item.keys():
                text_obj.whatsThis = gear_spec_item["description"]
                text_obj.setToolTip(gear_spec_item["description"])
