# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlg_config(object):
    def setupUi(self, dlg_config):
        dlg_config.setObjectName("dlg_config")
        dlg_config.resize(341, 269)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlg_config)
        self.buttonBox.setGeometry(QtCore.QRect(110, 230, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(dlg_config)
        self.label.setGeometry(QtCore.QRect(55, 22, 37, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(dlg_config)
        self.label_2.setGeometry(QtCore.QRect(20, 48, 72, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(dlg_config)
        self.label_3.setGeometry(QtCore.QRect(61, 74, 31, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(dlg_config)
        self.label_4.setGeometry(QtCore.QRect(54, 152, 38, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(dlg_config)
        self.label_5.setGeometry(QtCore.QRect(45, 100, 47, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(dlg_config)
        self.label_6.setGeometry(QtCore.QRect(39, 126, 53, 16))
        self.label_6.setObjectName("label_6")
        self.lst_enum = QtWidgets.QListWidget(dlg_config)
        self.lst_enum.setGeometry(QtCore.QRect(100, 150, 171, 81))
        self.lst_enum.setObjectName("lst_enum")
        self.btn_add = QtWidgets.QPushButton(dlg_config)
        self.btn_add.setGeometry(QtCore.QRect(270, 150, 51, 32))
        self.btn_add.setObjectName("btn_add")
        self.btn_edit = QtWidgets.QPushButton(dlg_config)
        self.btn_edit.setGeometry(QtCore.QRect(270, 175, 51, 32))
        self.btn_edit.setObjectName("btn_edit")
        self.btn_del = QtWidgets.QPushButton(dlg_config)
        self.btn_del.setGeometry(QtCore.QRect(270, 200, 51, 32))
        self.btn_del.setObjectName("btn_del")
        self.widget = QtWidgets.QWidget(dlg_config)
        self.widget.setGeometry(QtCore.QRect(100, 21, 171, 121))
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setLabelAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.ck_optional = QtWidgets.QCheckBox(self.widget)
        self.ck_optional.setText("")
        self.ck_optional.setObjectName("ck_optional")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.LabelRole, self.ck_optional)
        self.cbo_type = QtWidgets.QComboBox(self.widget)
        self.cbo_type.setObjectName("cbo_type")
        self.cbo_type.addItem("")
        self.cbo_type.addItem("")
        self.cbo_type.addItem("")
        self.cbo_type.addItem("")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.SpanningRole, self.cbo_type)
        self.txt_default = QtWidgets.QLineEdit(self.widget)
        self.txt_default.setObjectName("txt_default")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.SpanningRole, self.txt_default)
        self.txt_description = QtWidgets.QLineEdit(self.widget)
        self.txt_description.setObjectName("txt_description")
        self.formLayout.setWidget(
            1,
            QtWidgets.QFormLayout.SpanningRole,
            self.txt_description)
        self.txt_name = QtWidgets.QLineEdit(self.widget)
        self.txt_name.setObjectName("txt_name")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.SpanningRole, self.txt_name)

        self.retranslateUi(dlg_config)
        self.buttonBox.accepted.connect(dlg_config.accept)
        self.buttonBox.rejected.connect(dlg_config.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_config)

    def retranslateUi(self, dlg_config):
        _translate = QtCore.QCoreApplication.translate
        dlg_config.setWindowTitle(
            _translate(
                "dlg_config",
                "Add or Edit Configs"))
        self.label.setText(_translate("dlg_config", "name:"))
        self.label_2.setText(_translate("dlg_config", "description:"))
        self.label_3.setText(_translate("dlg_config", "type:"))
        self.label_4.setText(_translate("dlg_config", "enum:"))
        self.label_5.setText(_translate("dlg_config", "default:"))
        self.label_6.setText(_translate("dlg_config", "optional:"))
        self.btn_add.setText(_translate("dlg_config", "Add"))
        self.btn_edit.setText(_translate("dlg_config", "Edit"))
        self.btn_del.setText(_translate("dlg_config", "Del"))
        self.cbo_type.setItemText(0, _translate("dlg_config", "string"))
        self.cbo_type.setItemText(1, _translate("dlg_config", "number"))
        self.cbo_type.setItemText(2, _translate("dlg_config", "integer"))
        self.cbo_type.setItemText(3, _translate("dlg_config", "boolean"))
