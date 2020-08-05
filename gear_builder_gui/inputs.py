# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inputs.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlg_inputs(object):
    def setupUi(self, dlg_inputs):
        dlg_inputs.setObjectName("dlg_inputs")
        dlg_inputs.resize(349, 276)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlg_inputs)
        self.buttonBox.setGeometry(QtCore.QRect(110, 230, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(dlg_inputs)
        self.formLayoutWidget.setGeometry(QtCore.QRect(50, 40, 271, 151))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txt_name = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.txt_name.setObjectName("txt_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_name)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.txt_description = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.txt_description.setObjectName("txt_description")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_description)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.cbo_base = QtWidgets.QComboBox(self.formLayoutWidget)
        self.cbo_base.setObjectName("cbo_base")
        self.cbo_base.addItem("")
        self.cbo_base.addItem("")
        self.cbo_base.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cbo_base)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.cbo_type = QtWidgets.QComboBox(self.formLayoutWidget)
        self.cbo_type.setObjectName("cbo_type")
        self.cbo_type.addItem("")
        self.cbo_type.addItem("")
        self.cbo_type.addItem("")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cbo_type)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.ck_optional = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.ck_optional.setText("")
        self.ck_optional.setObjectName("ck_optional")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.ck_optional)

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
        self.cbo_base.setItemText(0, _translate("dlg_inputs", "file"))
        self.cbo_base.setItemText(1, _translate("dlg_inputs", "context"))
        self.cbo_base.setItemText(2, _translate("dlg_inputs", "api-key"))
        self.label_4.setText(_translate("dlg_inputs", "type:"))
        self.cbo_type.setItemText(0, _translate("dlg_inputs", "None"))
        self.cbo_type.setItemText(1, _translate("dlg_inputs", "nifti"))
        self.cbo_type.setItemText(2, _translate("dlg_inputs", "dicom"))
        self.label_5.setText(_translate("dlg_inputs", "optional:"))
