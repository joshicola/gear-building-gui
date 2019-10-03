from config import  Ui_dlg_config
from PyQt5 import QtWidgets

class config_dialog(QtWidgets.QDialog):
    def __init__(self,parent=None,cbo_val=None):
        super(config_dialog,self).__init__(parent)
        self.ui = Ui_dlg_config()
        self.ui.setupUi(self)
        self.ui.btn_add.clicked.connect(self.add_enum)
        self.ui.btn_edit.clicked.connect(self.edit_enum)
        self.ui.btn_del.clicked.connect(self.del_enum)
        if cbo_val!=None:
            name, editD = cbo_val
            self.ui.txt_name.setText(name)
            for key in editD.keys():
                if key == 'type':
                    obj = eval('self.ui.cbo_'+key)
                    i = obj.findText(editD[key])
                    obj.setCurrentIndex(i)
                elif key == 'enum':
                    obj = eval('self.ui.lst_'+key)
                    obj.clear()
                    obj.addItems(editD[key])
                elif key == 'default':
                    obj = self.ui.txt_default
                    obj.setText(editD[key])               
                elif key == 'description':
                    obj = self.ui.txt_description
                    obj.setText(editD[key])
                elif key == 'optional':
                    obj = self.ui.ck_optional
                    obj.setChecked(editD[key])

    def add_enum(self):
        text, ok = QtWidgets.QInputDialog.getText(self,"Enter Value",'Enter Value')
        if ok:
            self.ui.lst_enum.addItem(text)

    def edit_enum(self):
        item = self.ui.lst_enum.currentItem()
        if item != None:
            text = item.text()
            text_upd, ok = QtWidgets.QInputDialog.getText(self,"Enter Value","Enter Value", text=text)
            if ok:
                item.setText(text_upd)
    def del_enum(self):
        obj = self.ui.lst_enum
        i = obj.currentIndex()
        if i!=None:
            obj.takeItem(i.row())

    def cbo_value(self):
        name = self.ui.txt_name.text()
        data = {}
        data['description'] = self.ui.txt_description.text()
        data['type'] = self.ui.cbo_type.currentText()
        data['optional'] = self.ui.ck_optional.isChecked()
        default = self.ui.txt_default.text()

        # Only set 'default' if not optional and there is something there
        if (len(default)>0) and (not data['optional']):
            data['default'] = default

        #grab list of enumerated values, if not empty    
        obj = self.ui.lst_enum
        if obj.count()>0:
            items = []
            for i in range(obj.count()):
                items.append(obj.item(i).text())
            data['enum'] = items

        return [name,data]

    @staticmethod
    def get_data(parent=None,cbo_val=None):
        dialog = config_dialog(parent,cbo_val)
        ret_val = dialog.exec_()
        if ret_val:
            return dialog.cbo_value()
        else:
            return [None,None]