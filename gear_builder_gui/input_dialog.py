import os
import os.path as op

from PyQt5 import QtCore, QtGui, QtWidgets, uic


class input_dialog(QtWidgets.QDialog):
    """
    Dialog box class representing common options for a gear file input.
    """

    def __init__(self, parent=None, cbo_val=None):
        """
        Dialog box representing common options for a gear file input.

        Args:
            parent (object, optional): Parent of dialog. Defaults to None.
            cbo_val (tuple, optional): A name, data tuple to initialize the
                confiuration dialog. Defaults to None.
        """
        super(input_dialog, self).__init__(parent)
        dialog_ui_path = op.join(
            op.dirname(os.path.realpath(__file__)), "pyqt5_ui/inputs.ui"
        )
        Form, _ = uic.loadUiType(dialog_ui_path)
        # self.ui = Ui_dlg_config()
        self.ui = Form()
        self.ui.setupUi(self)
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
            name, editD = cbo_val
            self.ui.txt_name.setText(name)
            for key in editD.keys():
                if key == "base":
                    obj = eval("self.ui.cbo_" + key)
                    i = obj.findText(editD[key])
                    obj.setCurrentIndex(i)
                elif key == "type":
                    obj = eval("self.ui.cbo_" + key)
                    i = obj.findText(editD[key]["enum"][0])
                    obj.setCurrentIndex(i)
                elif key == "description":
                    obj = self.ui.txt_description
                    obj.setText(editD[key])
                elif key == "optional":
                    obj = self.ui.ck_optional
                    obj.setChecked(editD[key])

    def cbo_value(self):
        """
        Returns a collated name/data tuple representing the input.

        Returns:
            tuple: A name/data tuple describing the file input.
        """
        name = self.ui.txt_name.text()
        data = {}
        data["description"] = self.ui.txt_description.text()
        data["base"] = self.ui.cbo_base.currentText()
        if (data["base"] == "file") and (self.ui.cbo_type.currentText() != "None"):
            data["type"] = {"enum": [self.ui.cbo_type.currentText()]}

        data["optional"] = self.ui.ck_optional.isChecked()
        return [name, data]

    def changed_name(self):
        """
        Check the input name for length. Enable OK button if greater than zero.
        """
        # We will not allow for a config name to be less than 1 character
        txt_name = self.ui.txt_name
        btn = self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        if len(txt_name.text()) < 1:
            btn.setEnabled(False)
        else:
            btn.setEnabled(True)

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
        dialog = input_dialog(parent, cbo_val)
        ret_val = dialog.exec_()
        if ret_val:
            return dialog.cbo_value()
        else:
            return (None, None)
