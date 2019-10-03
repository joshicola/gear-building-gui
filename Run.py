from PyQt5 import QtWidgets
from manifest import Ui_MainWindow
from input_dialog import input_dialog
from config_dialog import config_dialog
import sys
import json

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
        self.ui.btn_make_manifest.clicked.connect(self.save_manifest)
    
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
        # edit this later utility/analysis
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
        inputs = {}
        cbo_obj = self.ui.cmbo_inputs
        for i in range(cbo_obj.count()):
            inputs[cbo_obj.itemText(i)] = cbo_obj.itemData(i)

        manifest['inputs'] = inputs

        # Build config section
        config = {}
        cbo_obj = self.ui.cmbo_config
        for i in range(cbo_obj.count()):
            config[cbo_obj.itemText(i)] = cbo_obj.itemData(i)

        manifest['config'] = config
        # The command
        manifest['command'] = '/flywheel/v0/run.py'

        json.dump(manifest,open('manifest.json','w'),indent=2)

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())