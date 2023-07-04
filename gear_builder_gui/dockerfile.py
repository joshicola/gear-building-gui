import json
from pathlib import Path

import pystache
from PyQt6 import QtWidgets


class Dockerfile:
    """
    This class manages the definition and writing of a draft Dockerfile.
    """

    def __init__(self, main_window):
        """
        Initialize members, methods, and UI hooks

        Args:
            main_window (GearBuilderGUI): The instantiated main window
        """
        self.dockerfile_def = main_window.gear_def["dockerfile"]
        self.main_window = main_window
        self.ui = main_window.ui
        self.ui.btn_APT_add.clicked.connect(self.add_row)
        self.ui.btn_APT_del.clicked.connect(self.del_row)
        # Set the APT table to select row only
        self.ui.tblAPT.setSelectionBehavior(
            QtWidgets.QTableWidget.SelectionBehavior.SelectRows
        )
        self.ui.btn_PIP_add.clicked.connect(self.add_row)
        self.ui.btn_PIP_del.clicked.connect(self.del_row)
        # Set the PIP table to select row only
        self.ui.tblPIP.setSelectionBehavior(
            QtWidgets.QTableWidget.SelectionBehavior.SelectRows
        )
        self.ui.btn_ENV_add.clicked.connect(self.add_row)
        self.ui.btn_ENV_del.clicked.connect(self.del_row)
        # Set the ENV table to select row only
        self.ui.tblENV.setSelectionBehavior(
            QtWidgets.QTableWidget.SelectionBehavior.SelectRows
        )

        # Set Docker maintainer label to match manifest
        self.ui.txt_maintainer_2.textChanged.connect(self._update_maintainers)
        self.ui.txt_maintainer_2.maxLength = self.ui.txt_maintainer.maxLength

    def _update_dockerfile_def_from_form(self):
        """
        Update the dockerfile_def dictionary from the form fields.

        TODO: Create update_form_from_dockerfile_def procedure for loading the
            dockerfile_def from a gear configuration file (<gear_name>.config.json??)
        """
        self.dockerfile_def["FROM"] = self.ui.cbo_docker_source.currentText()
        self.dockerfile_def["Maintainer"] = self.ui.txt_maintainer.text()

        self.dockerfile_def["apt_get"] = []
        tblAPT = self.ui.tblAPT
        for i in range(tblAPT.rowCount()):
            package = {}
            package["name"] = tblAPT.item(i, 0).text()
            version = tblAPT.item(i, 1).text()
            if len(version) > 0:
                package["version"] = version
            self.dockerfile_def["apt_get"].append(package)

        self.dockerfile_def["pip"] = []
        tblPIP = self.ui.tblPIP
        for i in range(tblPIP.rowCount()):
            package = {}
            package["name"] = tblPIP.item(i, 0).text()
            version = tblPIP.item(i, 1).text()
            if len(version) > 0:
                package["version"] = version
            self.dockerfile_def["pip"].append(package)

        self.dockerfile_def["ENV"] = []
        tblENV = self.ui.tblENV
        for i in range(tblENV.rowCount()):
            ENV = {}
            ENV["name"] = tblENV.item(i, 0).text()
            ENV["value"] = tblENV.item(i, 1).text()
            self.dockerfile_def["ENV"].append(ENV)

    def load_dockerfile_from_file(self):
        """
        Load Dockerfile from file.
        """
        dockerfile_file = QtWidgets.QFileDialog.getOpenFileName(
            self.main_window, "Select Dockerfile to load.", filter="Dockerfile"
        )

        # TODO: Should I warn about replacement of all Dockerfile values?
        if len(dockerfile_file[0]) > 0:
            with open(dockerfile_file[0], "r") as dockerfile_raw:
                dockerfile = json.load(dockerfile_raw)
            self._update_form_from_dockerfile()

    def _update_form_from_dockerfile(self):
        """
        Update form values from loaded dockerfile_def dictionary.
        """
        try:
            # Set combo box to value specified if exists, otherwise add a new value.
            from_index = self.ui.cbo_docker_source.findText(self.dockerfile_def["FROM"])
            if from_index != -1:
                self.ui.cbo_docker_source.setCurrentIndex(from_index)
            else:
                self.ui.cbo_docker_source.addItem(self.dockerfile_def["FROM"])
                self.ui.cbo_docker_source.setCurrentText(self.dockerfile_def["FROM"])
            self.ui.txt_maintainer.setText(self.dockerfile_def["Maintainer"])

            self.ui.tblAPT.setRowCount(0)
            for i, package in enumerate(self.dockerfile_def["apt_get"]):
                self.ui.tblAPT.insertRow(i)
                self.ui.tblAPT.setItem(
                    i, 0, QtWidgets.QTableWidgetItem(package.get("name", ""))
                )
                self.ui.tblAPT.setItem(
                    i, 1, QtWidgets.QTableWidgetItem(package.get("version", ""))
                )

            self.ui.tblPIP.setRowCount(0)
            for i, package in enumerate(self.dockerfile_def["pip"]):
                self.ui.tblPIP.insertRow(i)
                self.ui.tblPIP.setItem(
                    i, 0, QtWidgets.QTableWidgetItem(package.get("name", ""))
                )
                self.ui.tblPIP.setItem(
                    i, 1, QtWidgets.QTableWidgetItem(package.get("version", ""))
                )

            self.ui.tblENV.setRowCount(0)
            for i, package in enumerate(self.dockerfile_def["ENV"]):
                self.ui.tblENV.insertRow(i)
                self.ui.tblENV.setItem(
                    i, 0, QtWidgets.QTableWidgetItem(package.get("name", ""))
                )
                self.ui.tblENV.setItem(
                    i, 1, QtWidgets.QTableWidgetItem(package.get("value", ""))
                )

        except Exception as e:
            print(e)

    def _update_maintainers(self):
        """
        An event-driven method to ensure that the manifest.maintainer and the
            dockerfile.maintainer are in sync.
        """
        if self.ui.txt_maintainer.text() is not self.ui.txt_maintainer_2.text():
            self.ui.txt_maintainer.setText(self.ui.txt_maintainer_2.text())

    # add functionality to the add/del docker ENV variables buttons
    def add_row(self):
        """
        Add row to the indicated table.
        """
        sender = self.main_window.sender()
        if "APT" in sender.objectName():
            obj = self.ui.tblAPT
        elif "ENV" in sender.objectName():
            obj = self.ui.tblENV
        elif "PIP" in sender.objectName():
            obj = self.ui.tblPIP
        else:
            obj = None

        if obj:
            rowPosition = obj.rowCount()
            obj.insertRow(rowPosition)

    def del_row(self):
        """
        Delete row from the indicated table.
        """
        sender = self.main_window.sender()
        if "APT" in sender.objectName():
            obj = self.ui.tblAPT
        elif "ENV" in sender.objectName():
            obj = self.ui.tblENV
        elif "PIP" in sender.objectName():
            obj = self.ui.tblPIP
        else:
            obj = None

        if obj:
            # get all selected indices
            selectedInds = obj.selectedIndexes()
            # parse through them for unique rows
            rows = []

            for ind in selectedInds:
                if ind.row() not in rows:
                    rows.append(ind.row())
            # make sure we iterate in reverse order!
            rows.sort(reverse=True)
            for row in rows:
                obj.removeRow(row)

    def save(self, directory, dockerfile_template=None):
        """
        Parse a dockerfile_template to a Dockerfile in the directory indicated.

        Args:
            directory (str): Path to output directory
            dockerfile_template (str, optional): Path to Dockerfile mustache template.
                Defaults to None.
        """
        directory = Path(directory)
        self._update_dockerfile_def_from_form()

        # if provided, use default dockerfile_template
        if dockerfile_template:
            self.dockerfile_def["dockerfile_template"] = dockerfile_template
        # else if not already loaded, use the default template
        elif not self.dockerfile_def.get("dockerfile_template"):
            dockerfile_template = "default_templates/Dockerfile.mu"
            self.dockerfile_def["dockerfile_template"] = dockerfile_template

        renderer = pystache.Renderer()

        # copy dictionary and add a section indicators
        dockerfile = self.dockerfile_def.copy()
        # Check for non-zero number of inputs
        if len(dockerfile["apt_get"]) > 0:
            dockerfile["has_apt"] = True

        # Check for a non-zero number of configs
        if len(dockerfile["pip"]) > 0:
            dockerfile["has_pip"] = True

        # Check for a non-zero number of configs
        if len(dockerfile["ENV"]) > 0:
            dockerfile["has_env"] = True

        if dockerfile["has_pip"]:

            requirements_template = "default_templates/requirements.txt.mu"

            template_output = renderer.render_path(
                self.main_window.root_dir / requirements_template,
                {"dockerfile": dockerfile},
            )

            with open(directory / "requirements.txt", "w") as fp:
                fp.write(template_output)

        output = renderer.render_path(
            self.main_window.root_dir / self.dockerfile_def["dockerfile_template"],
            {"dockerfile": dockerfile},
        )

        # This gets rid of the last line continuation character in iterated elements
        output = output.replace(" \\\n*", "\n")

        with open(directory / "Dockerfile", "w") as fp:
            fp.write(output)
