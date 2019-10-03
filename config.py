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
        dlg_config.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlg_config)
        self.buttonBox.setGeometry(QtCore.QRect(110, 230, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(dlg_config)
        self.buttonBox.accepted.connect(dlg_config.accept)
        self.buttonBox.rejected.connect(dlg_config.reject)
        QtCore.QMetaObject.connectSlotsByName(dlg_config)

    def retranslateUi(self, dlg_config):
        _translate = QtCore.QCoreApplication.translate
        dlg_config.setWindowTitle(_translate("dlg_config", "Dialog"))

