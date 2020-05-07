from PyQt5 import QtCore, QtGui, QtWidgets

from .config import Ui_dlg_config


class config_dialog(QtWidgets.QDialog):
    def __init__(self, parent=None, cbo_val=None):
        super(config_dialog, self).__init__(parent)
        # "name" and "data" represent the name and data of a config item.
        # The extra, non-standard tags will be preserved
        self.name = ""
        self.data = {}
        self.ui = Ui_dlg_config()
        self.ui.setupUi(self)
        self.ui.ck_default.setVisible(False)
        self.ui.cbo_type.currentIndexChanged.connect(self.type_changed)
        self.ui.btn_add.clicked.connect(self.add_enum)
        self.ui.btn_edit.clicked.connect(self.edit_enum)
        self.ui.btn_del.clicked.connect(self.del_enum)
        self.ui.txt_name.textChanged.connect(self.changed_name)
        # disable OK button on create.
        btn = self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        btn.setEnabled(False)
        # Create a validation protocol
        self.ui.txt_name.maxLength = 30
        rx = QtCore.QRegExp("^[a-z0-9\\-\\_]+$")
        val = QtGui.QRegExpValidator(rx, self)
        self.ui.txt_name.setValidator(val)
        if cbo_val is not None:
            self.name, self.data = cbo_val
            self.ui.txt_name.setText(self.name)
            for key in self.data.keys():
                if key == 'type':
                    obj = eval('self.ui.cbo_' + key)
                    i = obj.findText(self.data[key])
                    obj.setCurrentIndex(i)
                    if self.data[key] == 'boolean':
                        self.ui.ck_default.setVisible(True)
                        self.ui.txt_default.setVisible(False)
                    else:
                        self.ui.ck_default.setVisible(False)
                        self.ui.txt_default.setVisible(True)
                elif key == 'enum':
                    obj = eval('self.ui.lst_' + key)
                    obj.clear()
                    obj.addItems(self.data[key])
                elif key == 'default':
                    if self.data['type'] is not 'boolean':
                        obj = self.ui.txt_default
                        obj.setText(str(self.data[key]))
                    else:
                        obj = self.ui.ck_default
                        self.ui.ck_default.setChecked(self.data[key])
                elif key == 'description':
                    obj = self.ui.txt_description
                    obj.setText(self.data[key])
                elif key == 'optional':
                    obj = self.ui.ck_optional
                    obj.setChecked(self.data[key])

    def type_changed(self):
        obj = self.ui.cbo_type
        if obj.currentText() == 'boolean':
            self.ui.ck_default.setVisible(True)
            self.ui.txt_default.setVisible(False)
            # validate contents as boolean or set a default value
            if self.ui.txt_default.text() in ['True', 'true']:
                self.ui.ck_default.setChecked(True)
            else:
                self.ui.ck_default.setChecked(False)
        else:
            self.ui.ck_default.setVisible(False)
            self.ui.txt_default.setVisible(True)
            text_obj = self.ui.txt_default
            # check for valid type and set validator accordingly
            if obj.currentText() == 'integer':
                if not self.ui.txt_default.text().isdigit():
                    self.ui.txt_default.setText('0')
                rx = QtCore.QRegExp('^([0-9]+)$')
                val = QtGui.QRegExpValidator(rx, self)
                text_obj.setValidator(val)
            elif obj.currentText() == 'number':
                try:
                    float(self.ui.txt_default.text())
                except ValueError:
                    self.ui.txt_default.setText('0.0')
                rx = QtCore.QRegExp('^([0-9]+)\\.([0-9]+)$')
                val = QtGui.QRegExpValidator(rx, self)
                text_obj.setValidator(val)
            else:
                rx = QtCore.QRegExp('.+')
                val = QtGui.QRegExpValidator(rx, self)
                text_obj.setValidator(val)

    def add_enum(self):
        text, ok = QtWidgets.QInputDialog.getText(
            self, "Enter Value", 'Enter Value')
        if ok:
            self.ui.lst_enum.addItem(text)

    def edit_enum(self):
        item = self.ui.lst_enum.currentItem()
        if item is not None:
            text = item.text()
            text_upd, ok = QtWidgets.QInputDialog.getText(
                self, "Enter Value", "Enter Value", text=text)
            if ok:
                item.setText(text_upd)

    def del_enum(self):
        obj = self.ui.lst_enum
        i = obj.currentIndex()
        if i is not None:
            obj.takeItem(i.row())

    def changed_name(self):
        # We will not allow for a config name to be less than 1 character
        txt_name = self.ui.txt_name
        btn = self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        if len(txt_name.text()) < 1:
            btn.setEnabled(False)
        else:
            btn.setEnabled(True)

    def cbo_value(self):
        self.name = self.ui.txt_name.text()

        self.data['description'] = self.ui.txt_description.text()
        self.data['type'] = self.ui.cbo_type.currentText()
        self.data['optional'] = self.ui.ck_optional.isChecked()

        default = self.ui.txt_default.text()

        # Only set 'default' if not optional and there is something there
        if (len(default) > 0) and (not self.data['optional']):
            if self.data['type'] == 'boolean':
                default = self.ui.ck_default.isChecked()
            elif self.data['type'] == 'number':
                default = float(default)
            elif self.data['type'] == 'integer':
                default = int(default)
            self.data['default'] = default
            self.data.pop('optional')

        # grab list of enumerated values, if not empty
        obj = self.ui.lst_enum
        if obj.count() > 0:
            items = []
            for i in range(obj.count()):
                items.append(obj.item(i).text())
            self.data['enum'] = items

        return [self.name, self.data]

    @staticmethod
    def get_data(parent=None, cbo_val=None):
        dialog = config_dialog(parent, cbo_val)
        ret_val = dialog.exec_()
        if ret_val:
            return dialog.cbo_value()
        else:
            return [None, None]
