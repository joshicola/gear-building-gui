import json
import os
import os.path as op

from PyQt5 import QtCore, QtGui, QtWidgets


class Dockerfile():
    def __init__(self, main_window):
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

    def save(self, directory):
        dockerstrings = []
        dockerstrings.extend([
            '# Dockerfile exported by GearBuilderGUI.' +
            'Stash edits before export again', ''
        ])
        # export FROM statement
        text_obj = self.ui.cbo_docker_source
        dockerstrings.extend([
            '# Inheriting from established docker image:',
            'FROM ' + text_obj.currentText(),
            ''
        ])
        # Export LABEL Maintainer
        text_obj = self.ui.txt_maintainer
        dockerstrings.extend([
            '# Inheriting from established docker image:',
            'LABEL maintainer="{}"'.format(text_obj.text()),
            ''
        ])
        ##########
        # Section for installing apt and pip dependencies
        # What version of python... etc....
        ##########

        #######################################################################
        # Specify APT dependencies
        # TODO: I may want to parse a packages.list file
        APTs = ['# Install APT dependencies']
        APTs.extend([
            'RUN apt-get update && \\',
            '    apt-get install -y --no-install-recommends \\'
        ])
        obj = self.ui.tblAPT
        for i in range(obj.rowCount()):
            Package = obj.item(i, 0).text()
            Version = obj.item(i, 1).text()
            line = '    {}{} '.format(Package, Version)
            if i == (obj.rowCount() - 1):
                line += '&&'
            line += ' \\ '
            APTs.append(line)
        APTs.extend(['    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*', ''])
        dockerstrings.extend(APTs)

        #######################################################################
        # Specify PIP dependencies
        # TODO: I may want to parse a 'requirements.txt' file
        # TODO: I may want to have a dialog for this section... Not allowing to add a package without a specific
        # version... that is formatted and validated according to semantic versioning.
        obj = self.ui.tblPIP
        if obj.rowCount() > 0:
            PIPs = ['# Install PIP Dependencies']
            PIPs.extend([
                'COPY requirements.txt requirements.txt',
                'RUN pip3 install --upgrade pip && \\ ',
                '    pip install -r requirements.txt\\ ',
                '    rm -rf /root/.cache/pip',
                ''
            ])

            requirements_txt = open(
                op.join(directory, 'requirements.txt'), 'w')
            lines = []
            for i in range(obj.rowCount()):
                Package = obj.item(i, 0).text()
                Version = obj.item(i, 1).text()
                line = '{}=={}\n'.format(Package, Version)
                lines.append(line)
                # Gosh this is sloppy!!!!
                # TODO: is there a validator for this?
                # Yes, we can validate on semantic versioning...
                if len(Version) < 1:
                    print('Versioning is strictly enforced.')
                    return -1
            requirements_txt.writelines(lines)

            dockerstrings.extend(PIPs)

        #######################################################################
        # Specify ENV Variables
        # TODO: I may want to parse a 'gear_environ.json' file
        # TODO: the ENV conversation with regards to how much they are included into the manifest (internal/external)
        ENVs = ['# Specify ENV Variables']
        ENVs.extend([
            'ENV \\ '
        ])
        obj = self.ui.tblENV
        for i in range(obj.rowCount()):
            Variable = obj.item(i, 0).text()
            Value = obj.item(i, 1).text()
            env_var = '    {}={} '.format(Variable, Value)
            if i < (obj.rowCount() - 1):
                env_var = env_var + ' \\ '
            ENVs.append(env_var)
        ENVs.extend([''])
        dockerstrings.extend(ENVs)

        # # Export Flywheel Spec
        dockerstrings.extend([
            '# Make directory for flywheel spec (v0):',
            'ENV FLYWHEEL /flywheel/v0',
            'WORKDIR ${FLYWHEEL}'
        ])

        # Gears will always have a 'run.py' and a 'manifest'
        # 'run.py' can be a "simple script" or a driver script for
        # the 'utils' package
        dockerstrings.extend([
            '# Copy executable/manifest to Gear',
            'COPY run.py ${FLYWHEEL}/run.py',
            'COPY manifest.json ${FLYWHEEL}/manifest.json', ''
        ])

        # If not a simple script, include utils:
        # TODO: This may need to have tighter integration with the script_management module to
        # determine which subdirectories to include
        if False:
            dockerstrings.extend([
                'COPY utils ${FLYWHEEL}/utils', ''
            ])

        # Preserve environment variables for Flywheel engine
        dockerstrings.extend([
            '# ENV preservation for Flywheel Engine',
            "RUN python -c 'import os, json; " +
            "f = open(\"/tmp/gear_environ.json\", \"w\");" +
            "json.dump(dict(os.environ), f)'", ''
        ])

        # Endpoint
        dockerstrings.extend({
            '# Configure entrypoint',
            'ENTRYPOINT ["/flywheel/v0/run.py"]'
        })

        dockerfile = open(
            op.join(directory, 'Dockerfile'),
            'w'
        )
        dockerfile.write('\n'.join(dockerstrings))
        dockerfile.close()
        return 0
