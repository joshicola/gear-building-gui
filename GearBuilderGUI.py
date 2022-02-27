#!/usr/bin/env python3
import json
import os
import os.path as op
import sys
from pathlib import Path

from PyQt5 import QtGui, QtWidgets, uic

from gear_builder_gui.dockerfile import Dockerfile
from gear_builder_gui.manifest import Manifest
from gear_builder_gui.menus import Gear_Builder_Menus
from gear_builder_gui.template_management import Template_Management


class GearBuilderGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GearBuilderGUI, self).__init__()
        self.root_dir = Path(op.dirname(__file__))
        # set gear definition to an empty default
        self.gear_def = {"manifest": {}, "dockerfile": {}, "template": {}}

        script_dir = op.dirname(os.path.realpath(__file__))
        icon_path = op.join(script_dir, "gear_builder_gui/resources/flywheel.png")
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowIconText("Flywheel Gear Builder")

        # This section is to load directly from the form object
        Form, _ = uic.loadUiType(
            op.join(script_dir, "gear_builder_gui/pyqt5_ui/gear_builder_gui.ui")
        )
        self.ui = Form()
        # This will load from a python file. Useful for direct debugging
        # self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Separating out functionality of the three components to facilitate
        # individual development
        self.manifest = Manifest(self)
        self.dockerfile = Dockerfile(self)
        self.templates = Template_Management(self)

        self.menus = Gear_Builder_Menus(self)

        self.ui.btn_export_gear.clicked.connect(self.export_gear)

    def save_gear_def(self, directory):
        gear_name = self.gear_def["manifest"]["name"]
        output_file = Path(directory) / (gear_name + ".gear.json")
        with open(output_file, "w") as fp:
            json.dump(self.gear_def, fp)

    def export_gear(self):
        directory = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select Folder to export gear template"
            )
        )
        if op.exists(directory):
            self.manifest._update_manifest_from_form()
            gear_path = Path(directory) / self.gear_def["manifest"]["name"]
            gear_path.mkdir(parents=True, exist_ok=True)
            self.manifest.save(gear_path)

            self.templates.render_and_copy_templates(gear_path)
            self.save_gear_def(gear_path)


if __name__ == "__main__":

    source_dir = Path(os.path.dirname(os.path.realpath(__file__)))
    app = QtWidgets.QApplication([])
    app.setWindowIcon(
        QtGui.QIcon(str(source_dir / "gear_builder_gui/resources/flywheel.png"))
    )
    application = GearBuilderGUI()
    application.show()
    sys.exit(app.exec())
