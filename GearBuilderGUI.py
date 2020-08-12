#!/usr/bin/env python3
import os
import os.path as op
import sys

from PyQt5 import QtGui, QtWidgets, uic

from gear_builder_gui.dockerfile import Dockerfile
from gear_builder_gui.manifest import Manifest
from gear_builder_gui.script_management import Script_Management


class GearBuilderGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GearBuilderGUI, self).__init__()

        # set gear configuration to default of empty
        self.gear_config = {"manifest": {}, "dockerfile": {}, "script": {}}

        script_dir = op.dirname(os.path.realpath(__file__))
        icon_path = op.join(script_dir, "gear_builder_gui/resources/flywheel.png")
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowIconText("Flywheel Gear Builder")

        Form, _ = uic.loadUiType(
            op.join(script_dir, "gear_builder_gui/pyqt5_ui/gear_builder_gui.ui")
        )
        self.ui = Form()
        self.ui.setupUi(self)

        # Separating out functionality of the three components to facilitate
        # individual development
        self.manifest = Manifest(self)
        self.dockerfile = Dockerfile(self)
        self.scripts = Script_Management(self)
        self.ui.btn_export_gear.clicked.connect(self.export_gear)

    # NOTE: This export of manifest, dockerfile, scripts works.
    # What else we might want is a means to save and load all of these settings.
    # That is, have entirely configured gear-builder templates that represent
    # exportible settings.  For now. Keep it simple.
    def export_gear(self):
        directory = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select Folder to export gear template"
            )
        )
        if op.exists(directory):
            self.manifest.save(directory)
            self.manifest.save_draft_readme(directory)
            self.dockerfile.save(directory)
            self.scripts.save(directory)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = GearBuilderGUI()
    application.show()
    sys.exit(app.exec())
