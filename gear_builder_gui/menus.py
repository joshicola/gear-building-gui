import json
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets


class Gear_Builder_Menus:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui

        self.menubar = self.main_window.menuBar()
        self.menubar.setNativeMenuBar(False)

        self.ui.actionExport_Gear.triggered.connect(main_window.export_gear)
        self.ui.actionLoad_Gear_Project.triggered.connect(self.load_gear_definition)
        self.ui.actionSave_Gear_Project.triggered.connect(self.save_gear_definition)

    def load_gear_definition(self):
        gear_def_filepath = QtWidgets.QFileDialog.getOpenFileName(
            self.main_window, "Load Gear Definition to file.", filter="*.gear.json"
        )
        if len(gear_def_filepath[0]) > 0:
            for key in ["manifest", "dockerfile", "template"]:
                self.main_window.gear_def[key].clear()
            with open(gear_def_filepath[0], "r") as fp:
                self.main_window.gear_def.update(json.load(fp))
            self.update_forms_from_gear_def()

    def update_forms_from_gear_def(self):
        gear_def = self.main_window.gear_def
        self.main_window.manifest.manifest = gear_def["manifest"]
        self.main_window.dockerfile.dockerfile_def = gear_def["dockerfile"]
        self.main_window.templates.template_def = gear_def["template"]

        self.main_window.manifest._update_form_from_manifest()
        self.main_window.dockerfile._update_form_from_dockerfile()
        self.main_window.templates._update_form_from_template_def()

    def save_gear_definition(self):
        self.main_window.manifest._update_manifest_from_form()
        self.main_window.dockerfile._update_dockerfile_def_from_form()
        self.main_window.templates._update_form_from_template_def()
        default_name = self.main_window.gear_def["manifest"]["name"] + ".gear.json"
        directory = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self.main_window, "Select Folder to save <gear name>.gear.json."
            )
        )

        if len(directory) > 0:
            gear_def_filepath = Path(directory) / default_name
            with open(gear_def_filepath, "w") as fp:
                json.dump(self.main_window.gear_def, fp)
