import os
import os.path as op

import pystache


class Dockerfile:
    def __init__(self, main_window):
        self.Dockerfile_def = {}
        self.ui = main_window.ui
        self.ui.btn_APT_add.clicked.connect(self.add_APT)
        self.ui.btn_APT_del.clicked.connect(self.del_APT)
        # Set the APT table to select row only
        self.ui.tblAPT.setSelectionBehavior(1)
        self.ui.btn_PIP_add.clicked.connect(self.add_PIP)
        self.ui.btn_PIP_del.clicked.connect(self.del_PIP)
        # Set the PIP table to select row only
        self.ui.tblPIP.setSelectionBehavior(1)
        self.ui.btn_ENV_add.clicked.connect(self.add_ENV)
        self.ui.btn_ENV_del.clicked.connect(self.del_ENV)
        # Set the ENV table to select row only
        self.ui.tblENV.setSelectionBehavior(1)

        # Set Docker maintainer label to match manifest
        self.ui.txt_maintainer_2.textChanged.connect(self.update_maintainers)
        self.ui.txt_maintainer_2.maxLength = self.ui.txt_maintainer.maxLength

    def update_Dockerfile_def(self):
        self.Dockerfile_def["FROM"] = self.ui.cbo_docker_source.currentText()
        self.Dockerfile_def["Maintainer"] = self.ui.txt_maintainer.text()

        self.Dockerfile_def["apt_get"] = []
        tblAPT = self.ui.tblAPT
        for i in range(tblAPT.rowCount()):
            package = {}
            package["name"] = tblAPT.item(i, 0).text()
            version = tblAPT.item(i, 1).text()
            if len(version) > 0:
                package["version"] = version
            self.Dockerfile_def["apt_get"].append(package)

        self.Dockerfile_def["pip"] = []
        tblPIP = self.ui.tblPIP
        for i in range(tblPIP.rowCount()):
            package = {}
            package["name"] = tblPIP.item(i, 0).text()
            version = tblPIP.item(i, 1).text()
            if len(version) > 0:
                package["version"] = version
            self.Dockerfile_def["pip"].append(package)

        self.Dockerfile_def["ENV"] = []
        tblENV = self.ui.tblENV
        for i in range(tblENV.rowCount()):
            ENV = {}
            ENV["name"] = tblENV.item(i, 0).text()
            ENV["value"] = tblENV.item(i, 1).text()
            self.Dockerfile_def["ENV"].append(ENV)

    def update_maintainers(self):
        if self.ui.txt_maintainer.text() is not self.ui.txt_maintainer_2.text():
            self.ui.txt_maintainer.setText(self.ui.txt_maintainer_2.text())

    def add_APT(self, obj):
        self.add_Row(self.ui.tblAPT)

    def del_APT(self, obj):
        self.del_Row(self.ui.tblAPT)

    def add_PIP(self, obj):
        self.add_Row(self.ui.tblPIP)

    def del_PIP(self, obj):
        self.del_Row(self.ui.tblPIP)

    def add_ENV(self, obj):
        self.add_Row(self.ui.tblENV)

    def del_ENV(self, obj):
        self.del_Row(self.ui.tblENV)

    # add functionality to the add/del docker ENV variables buttons
    def add_Row(self, obj):
        rowPosition = obj.rowCount()
        obj.insertRow(rowPosition)

    def del_Row(self, obj):
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

    def save(self, directory, Dockerfile_template=None):
        self.update_Dockerfile_def()
        if not Dockerfile_template:
            source_dir = op.join(
                os.path.dirname(os.path.realpath(__file__)), "..", "default_templates"
            )
            Dockerfile_template = op.join(source_dir, "Dockerfile.mu")
        renderer = pystache.Renderer()
        dockerfile = self.Dockerfile_def.copy()
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
            source_dir = op.join(
                os.path.dirname(os.path.realpath(__file__)), "..", "default_templates"
            )
            requirements_template = op.join(source_dir, "requirements.txt.mu")
            template_output = renderer.render_path(
                requirements_template, {"dockerfile": dockerfile}
            )

            with open(op.join(directory, "requirements.txt"), "w") as fp:
                fp.write(template_output)

        output = renderer.render_path(Dockerfile_template, {"dockerfile": dockerfile})

        # This gets rid of the last line continuation character in iterated elements
        output = output.replace(" \\\n*", "\n")

        with open(op.join(directory, "Dockerfile"), "w") as fp:
            fp.write(output)

        return 0
