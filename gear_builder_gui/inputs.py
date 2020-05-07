# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inputs.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlg_inputs(object):
    def setupUi(self, dlg_inputs):
        dlg_inputs.setObjectName("dlg_inputs")
        dlg_inputs.resize(373, 274)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlg_inputs)
        self.buttonBox.setGeometry(QtCore.QRect(110, 230, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.txt_name = QtWidgets.QLineEdit(dlg_inputs)
        self.txt_name.setGeometry(QtCore.QRect(110, 10, 113, 21))
        self.txt_name.setObjectName("txt_name")
        self.label = QtWidgets.QLabel(dlg_inputs)
        self.label.setGeometry(QtCore.QRect(10, 10, 60, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(dlg_inputs)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(dlg_inputs)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 41, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(dlg_inputs)
        self.label_4.setGeometry(QtCore.QRect(10, 110, 81, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(dlg_inputs)
        self.label_5.setGeometry(QtCore.QRect(10, 140, 81, 16))
        self.label_5.setObjectName("label_5")
        self.txt_description = QtWidgets.QLineEdit(dlg_inputs)
        self.txt_description.setGeometry(QtCore.QRect(110, 40, 113, 21))
        self.txt_description.setObjectName("txt_description")
        self.cbo_base = QtWidgets.QComboBox(dlg_inputs)
        self.cbo_base.setGeometry(QtCore.QRect(110, 70, 111, 26))
        self.cbo_base.setObjectName("cbo_base")
        self.cbo_base.addItem("")
        self.cbo_base.addItem("")
        self.cbo_base.addItem("")
        self.cbo_type = QtWidgets.QComboBox(dlg_inputs)
        self.cbo_type.setGeometry(QtCore.QRect(110, 100, 111, 26))
        self.cbo_type.setObjectName("cbo_type")
        self.cbo_type.addItem("")
        self.cbo_type.addItem("")
        self.cbo_type.addItem("")
        self.ck_optional = QtWidgets.QCheckBox(dlg_inputs)
        self.ck_optional.setGeometry(QtCore.QRect(110, 140, 87, 20))
        self.ck_optional.setObjectName("ck_optional")

        self.retranslateUi(dlg_inputs)
        self.buttonBox.rejected.connect(dlg_inputs.reject)
        self.buttonBox.accepted.connect(dlg_inputs.accept)
        QtCore.QMetaObject.connectSlotsByName(dlg_inputs)

    def retranslateUi(self, dlg_inputs):
        _translate = QtCore.QCoreApplication.translate
        dlg_inputs.setWindowTitle(_translate("dlg_inputs", "Add or Edit Inputs"))
        self.label.setText(_translate("dlg_inputs", "name:"))
        self.label_2.setText(_translate("dlg_inputs", "description:"))
        self.label_3.setText(_translate("dlg_inputs", "base:"))
        self.label_4.setText(_translate("dlg_inputs", "type:"))
        self.label_5.setText(_translate("dlg_inputs", "optional:"))
        self.cbo_base.setItemText(0, _translate("dlg_inputs", "file"))
        self.cbo_base.setItemText(1, _translate("dlg_inputs", "context"))
        self.cbo_base.setItemText(2, _translate("dlg_inputs", "api-key"))
        self.cbo_type.setItemText(0, _translate("dlg_inputs", "None"))
        self.cbo_type.setItemText(1, _translate("dlg_inputs", "nifti"))
        self.cbo_type.setItemText(2, _translate("dlg_inputs", "dicom"))
        self.ck_optional.setText(_translate("dlg_inputs", "optional"))
