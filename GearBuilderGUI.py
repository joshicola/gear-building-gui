from PyQt5 import QtWidgets
from gear_builder_gui.manifest import Ui_MainWindow
from gear_builder_gui.input_dialog import input_dialog
from gear_builder_gui.config_dialog import config_dialog
import sys
import json
import os, os.path as op

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_input_add.clicked.connect(self.add_input)
        self.ui.btn_input_edit.clicked.connect(self.edit_input)
        self.ui.btn_input_delete.clicked.connect(self.delete_input)
        self.ui.btn_config_add.clicked.connect(self.add_config)
        self.ui.btn_config_edit.clicked.connect(self.edit_config)
        self.ui.btn_config_delete.clicked.connect(self.delete_config)    
        self.ui.btn_save_manifest.clicked.connect(self.save_manifest)
        self.ui.btn_export_gear.clicked.connect(self.export_gear)
        self.ui.txt_maintainer.textChanged.connect(self.update_maintainers)
    
    def update_maintainers(self):
        self.ui.txt_maintainer_2.setText(
            self.ui.txt_maintainer.text()
        )
    
    # Add functionality to the input add/edit/deleted buttons
    def add_input(self):
        dialog = input_dialog()
        name, data = dialog.get_data()
        if name!=None:
            self.ui.cmbo_inputs.addItem(name,userData=data)
    
    def edit_input(self):
        obj = self.ui.cmbo_inputs
        name = obj.currentText()
        data = obj.currentData()
        dialog = input_dialog()
        name_upd, data = dialog.get_data(cbo_val=[name,data])
        if name_upd!=None:
            i = obj.findText(name)
            obj.setItemText(i,name_upd)
            obj.setItemData(i,data)

    def delete_input(self):
        i = self.ui.cmbo_inputs.currentIndex()
        self.ui.cmbo_inputs.removeItem(i)
        
    # add functionality to the add/edit/delete config buttons
    def add_config(self):
        dialog = config_dialog()
        name, data = dialog.get_data()
        if name!=None:
            self.ui.cmbo_config.addItem(name,userData=data)
    
    def edit_config(self):
        obj = self.ui.cmbo_config
        name = obj.currentText()
        data = obj.currentData()
        dialog = config_dialog()
        name_upd, data = dialog.get_data(cbo_val=[name,data])
        if name_upd!=None:
            i = obj.findText(name)
            obj.setItemText(i,name_upd)
            obj.setItemData(i,data)

    def delete_config(self):
        i = self.ui.cmbo_config.currentIndex()
        self.ui.cmbo_config.removeItem(i)

    def save_manifest(self):
        directory = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select Folder to save manifest.json"
            )
        )
        if len(directory)>0:
            self.save_manifest_to_dir(directory)

    def save_manifest_to_dir(self,directory):
        manifest = {}
        keys = [
            'name',
            'label',
            'description',
            'author',
            'maintainer',
            'license',
            'url',
            'source',
            'cite',
            'version'
        ]
        for key in keys:
            text_obj = eval('self.ui.txt_' + key)
            text_type = type(eval('self.ui.txt_' + key))
            if  text_type == QtWidgets.QPlainTextEdit:
                text_value = text_obj.toPlainText()
            else:
                text_value = text_obj.text()
            manifest[key] = text_value

        # Build Custom section
        custom = {}
        custom['docker-image'] = \
            'flywheel/' + manifest['name'] + ':' + manifest['version']
        gear_builder = {}
        # gear category on radio button
        if self.ui.rdo_analysis.isChecked():
            gear_builder['category'] = 'analysis'
        else:
             gear_builder['category'] = 'utility'
             
        gear_builder['image'] = custom['docker-image']
        
        custom['gear-builder'] = gear_builder
        # if "suite"
        if self.ui.chk_flywheel.isChecked():    
            flywheel = {}
            flywheel['suite'] = self.ui.txt_suite.text()
            custom['flywheel'] = flywheel

        manifest['custom'] = custom

        # Build inputs section
        # Each input item consists of the text (key) of a combo box and 
        # specifically constructed data (a dictionary).
        inputs = {}
        cbo_obj = self.ui.cmbo_inputs
        for i in range(cbo_obj.count()):
            inputs[cbo_obj.itemText(i)] = cbo_obj.itemData(i)

        manifest['inputs'] = inputs

        # Build config section
        # Each config item consists of the text (key) of a combo box and 
        # specifically constructed data (a dictionary).        
        config = {}
        cbo_obj = self.ui.cmbo_config
        for i in range(cbo_obj.count()):
            config[cbo_obj.itemText(i)] = cbo_obj.itemData(i)

        manifest['config'] = config
        # The command
        manifest['command'] = '/flywheel/v0/run.py'

        json.dump(
            manifest,
            open(op.join(directory,'manifest.json'),'w'),
            indent=2
        )
    
    def save_dockerfile_to_dir(self, directory):
        dockerstrings = []
        dockerstrings.extend([
            '# Dockerfile exported by GearBuilderGUI.' + \
            'Stash edits before export again',''
        ])
        # export FROM statement
        text_obj = self.ui.txt_docker_source
        dockerstrings.extend([
            '# Inheriting from established docker image:',
            'FROM ' + text_obj.text(), ''
        ])
        # Export LABEL Maintainer
        text_obj = self.ui.txt_maintainer
        dockerstrings.extend([
            '# Inheriting from established docker image:',
            'LABEL maintainer="{}"'.format(text_obj.text()), ''
        ])
        ##########
        # Section for installing apt and pip dependencies
        # What version of python... etc....
        ##########
        # # Export Flywheel Spec
        dockerstrings.extend([
            '# Make directory for flywheel spec (v0):',
            'ENV FLYWHEEL /flywheel/v0',
        ])
        
        # Gears will always have a 'run.py' and a 'manifest'
        # 'run.py' can be a "simple script" or a driver script for 
        # the 'utils' package
        dockerstrings.extend([
            '# Copy executable/manifest to Gear',
            'COPY run.py ${FLYWHEEL}/run.py',
            'COPY manifest.json ${FLYWHEEL}/manifest.json',''
        ])
        
        # If not a simple script, include utils:
        if False:
            dockerstrings.extend([
                'COPY utils ${FLYWHEEL}/utils',''
            ])
        
        # Preserve environment variables for Flywheel engine
        dockerstrings.extend([
            '# ENV preservation for Flywheel Engine',
            "RUN python -c 'import os, json; " + \
            "f = open(\"/tmp/gear_environ.json\", \"w\");" + \
            "json.dump(dict(os.environ), f)'",''
        ])
        
        # Endpoint
        dockerstrings.extend({
            '# Configure entrypoint',
            'ENTRYPOINT ["/flywheel/v0/run.py"]'
        })

        dockerfile = open(
            op.join(directory,'Dockerfile'),'w'
        )
        dockerfile.write('\n'.join(dockerstrings))
        dockerfile.close()

    def save_script_to_dir(self,directory):
        source_dir = os.path.dirname(os.path.realpath(__file__))
        is_simple_script = self.ui.ck_simple_script.isChecked()
        if is_simple_script:
            script_str = open(
                op.join(source_dir, 'script_library/simple_script/run.py'),
                'r'
            ).read()
            script_str = script_str.replace('{name}', self.ui.txt_name.text())
            script_str = script_str.replace(
                '{simple_script_name}', 
                self.ui.txt_simple_script.text()
            )

            out_file = open(op.join(directory,'run.py'),'w')
            out_file.write(script_str)
            out_file.close()

    def export_gear(self):
        directory = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select Folder to export gear template"
            )
        )
        self.save_manifest_to_dir(directory)
        self.save_dockerfile_to_dir(directory)
        self.save_script_to_dir(directory)

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())