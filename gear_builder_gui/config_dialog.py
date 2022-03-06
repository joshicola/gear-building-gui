import os
import os.path as op

from PyQt6 import QtCore, QtGui, QtWidgets, uic

# from .config import Ui_dlg_config


class config_dialog(QtWidgets.QDialog):
    """
    Dialog box class representing common options for a gear configuration.
    """

    def __init__(self, parent=None, cbo_val=None):
        """
        Dialog box representing common options for a gear configuration.

        Args:
            parent (object, optional): Parent of dialog. Defaults to None.
            cbo_val (tuple, optional): A name, data tuple to initialize the
                confiuration dialog. Defaults to None.
        """
        super(config_dialog, self).__init__(parent)
        # "name" and "data" represent the name and data of a config item.
        # The extra, non-standard tags will be preserved
        self.name = ""
        self.data = {}
        dialog_ui_path = op.join(
            op.dirname(os.path.realpath(__file__)), "pyqt5_ui/config.ui"
        )
        Form, _ = uic.loadUiType(dialog_ui_path)
        # self.ui = Ui_dlg_config()
        self.ui = Form()
        self.ui.setupUi(self)
        self.ui.ck_default.setVisible(False)
        self.ui.cbo_type.currentIndexChanged.connect(self.config_type_changed)
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
                if key == "type":
                    obj = eval("self.ui.cbo_" + key)
                    i = obj.findText(self.data[key])
                    obj.setCurrentIndex(i)
                    if self.data[key] == "boolean":
                        self.ui.ck_default.setVisible(True)
                        self.ui.lblDefault_bool.setVisible(True)
                        self.ui.txt_default.setVisible(False)
                        self.ui.lblDefault_txt.setVisible(False)
                    else:
                        self.ui.ck_default.setVisible(False)
                        self.ui.lblDefault_bool.setVisible(False)
                        self.ui.txt_default.setVisible(True)
                        self.ui.lblDefault_txt.setVisible(True)
                elif key == "enum":
                    obj = eval("self.ui.lst_" + key)
                    obj.clear()
                    obj.addItems(self.data[key])
                elif key == "default":
                    if self.data["type"] is not "boolean":
                        obj = self.ui.txt_default
                        obj.setText(str(self.data[key]))
                    else:
                        obj = self.ui.ck_default
                        self.ui.ck_default.setChecked(self.data[key])
                elif key == "description":
                    obj = self.ui.txt_description
                    obj.setText(self.data[key])
                elif key == "optional":
                    obj = self.ui.ck_optional
                    obj.setChecked(self.data[key])

    def config_type_changed(self):
        """
        Set visibility and type defaults on the type of config chosen
        """
        obj = self.ui.cbo_type
        if obj.currentText() == "boolean":
            self.ui.ck_default.setVisible(True)
            self.ui.lblDefault_bool.setVisible(True)
            self.ui.txt_default.setVisible(False)
            self.ui.lblDefault_txt.setVisible(False)
            # validate contents as boolean or set a default value
            if self.ui.txt_default.text() in ["True", "true"]:
                self.ui.ck_default.setChecked(True)
            else:
                self.ui.ck_default.setChecked(False)
        else:
            self.ui.ck_default.setVisible(False)
            self.ui.lblDefault_bool.setVisible(False)
            self.ui.txt_default.setVisible(True)
            self.ui.lblDefault_txt.setVisible(True)
            text_obj = self.ui.txt_default
            # check for valid type and set validator accordingly
            if obj.currentText() == "integer":
                if not self.ui.txt_default.text().isdigit():
                    self.ui.txt_default.setText("0")
                rx = QtCore.QRegExp("^([0-9]+)$")
                val = QtGui.QRegExpValidator(rx, self)
                text_obj.setValidator(val)
            elif obj.currentText() == "number":
                try:
                    float(self.ui.txt_default.text())
                except ValueError:
                    self.ui.txt_default.setText("0.0")
                rx = QtCore.QRegExp("^([0-9]+)\\.([0-9]+)$")
                val = QtGui.QRegExpValidator(rx, self)
                text_obj.setValidator(val)
            else:
                rx = QtCore.QRegExp(".+")
                val = QtGui.QRegExpValidator(rx, self)
                text_obj.setValidator(val)

    def add_enum(self):
        """
        Add an enumerated value to the list.
        """
        text, ok = QtWidgets.QInputDialog.getText(self, "Enter Value", "Enter Value")
        if ok:
            self.ui.lst_enum.addItem(text)

    def edit_enum(self):
        """
        Edit the selected enumerated value in the list.
        """
        item = self.ui.lst_enum.currentItem()
        if item is not None:
            text = item.text()
            text_upd, ok = QtWidgets.QInputDialog.getText(
                self, "Enter Value", "Enter Value", text=text
            )
            if ok:
                item.setText(text_upd)

    def del_enum(self):
        """
        Delete the selected enumerated value in the list.
        """
        obj = self.ui.lst_enum
        i = obj.currentIndex()
        if i is not None:
            obj.takeItem(i.row())

    def changed_name(self):
        """
        Check the config name for length. Enable OK button if greater than zero.
        """
        # We will not allow for a config name to be less than 1 character
        txt_name = self.ui.txt_name
        btn = self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        if len(txt_name.text()) < 1:
            btn.setEnabled(False)
        else:
            btn.setEnabled(True)

    def cbo_value(self):
        """
        Returns a collated name/data dictionary pair representing the config.

        Returns:
            tuple: A name/data pairing describing the config option.
        """
        self.name = self.ui.txt_name.text()

        self.data["description"] = self.ui.txt_description.text()
        self.data["type"] = self.ui.cbo_type.currentText()
        self.data["optional"] = self.ui.ck_optional.isChecked()

        default = self.ui.txt_default.text()

        # Only set 'default' if not optional and there is something there
        if (len(default) > 0) and (not self.data["optional"]):
            if self.data["type"] == "boolean":
                default = self.ui.ck_default.isChecked()
            elif self.data["type"] == "number":
                default = float(default)
            elif self.data["type"] == "integer":
                default = int(default)
            self.data["default"] = default
            self.data.pop("optional")

        # grab list of enumerated values, if not empty
        obj = self.ui.lst_enum
        if obj.count() > 0:
            items = []
            for i in range(obj.count()):
                items.append(obj.item(i).text())
            self.data["enum"] = items

        return (self.name, self.data)

    @staticmethod
    def get_data(parent=None, cbo_val=None):
        """
        Static method to initialize dialog box and retrieve the name/data pair.

        Args:
            parent (object, optional): Parent of dialog. Defaults to None.
            cbo_val (tuple, optional): Name/data pair to initialize dialog.
                Defaults to None.

        Returns:
            tuple: Name/data pair
        """

        dialog = config_dialog(parent, cbo_val)
        ret_val = dialog.exec_()
        if ret_val:
            return dialog.cbo_value()
        else:
            return (None, None)
