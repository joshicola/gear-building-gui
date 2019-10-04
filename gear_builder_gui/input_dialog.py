from .inputs import  Ui_dlg_inputs
from PyQt5 import QtWidgets

class input_dialog(QtWidgets.QDialog):
    def __init__(self,parent=None,cbo_val=None):
        super(input_dialog,self).__init__(parent)
        self.ui = Ui_dlg_inputs()
        self.ui.setupUi(self)
        if cbo_val!=None:
            name, editD = cbo_val
            self.ui.txt_name.setText(name)
            for key in editD.keys():
                if key == 'base':
                    obj = eval('self.ui.cbo_'+key)
                    i = obj.findText(editD[key])
                    obj.setCurrentIndex(i)
                elif key == 'type':
                    obj = eval('self.ui.cbo_'+key)
                    i = obj.findText(editD[key]["enum"][0])
                    obj.setCurrentIndex(i)                    
                elif key == 'description':
                    obj = self.ui.txt_description
                    obj.setText(editD[key])
                elif key == 'optional':
                    obj = self.ui.ck_optional
                    obj.setChecked(editD[key])


    def cbo_value(self):
        name = self.ui.txt_name.text()
        data = {}
        data['description'] = self.ui.txt_description.text()
        data['base'] = self.ui.cbo_base.currentText()
        if (data['base'] == 'file') and \
            (self.ui.cbo_type.currentText() != "None"):
            data['type'] = {"enum":[self.ui.cbo_type.currentText()]}

        data['optional'] = self.ui.ck_optional.isChecked()
        return [name,data]

    @staticmethod
    def get_data(parent=None,cbo_val=None):
        dialog = input_dialog(parent,cbo_val)
        ret_val = dialog.exec_()
        if ret_val:
            return dialog.cbo_value()
        else:
            return [None,None]