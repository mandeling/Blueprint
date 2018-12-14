# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './VariableDetail.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(248, 360)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_var_type = QtWidgets.QLabel(Form)
        self.label_var_type.setObjectName("label_var_type")
        self.gridLayout.addWidget(self.label_var_type, 1, 0, 1, 1)
        self.lineEdit_var_name = QtWidgets.QLineEdit(Form)
        self.lineEdit_var_name.setObjectName("lineEdit_var_name")
        self.gridLayout.addWidget(self.lineEdit_var_name, 0, 1, 1, 1)
        self.label_var_name = QtWidgets.QLabel(Form)
        self.label_var_name.setObjectName("label_var_name")
        self.gridLayout.addWidget(self.label_var_name, 0, 0, 1, 1)
        self.label_var_value = QtWidgets.QLabel(Form)
        self.label_var_value.setObjectName("label_var_value")
        self.gridLayout.addWidget(self.label_var_value, 2, 0, 1, 1)
        self.lineEdit_var_value = QtWidgets.QLineEdit(Form)
        self.lineEdit_var_value.setObjectName("lineEdit_var_value")
        self.gridLayout.addWidget(self.lineEdit_var_value, 2, 1, 1, 1)
        self.comboBox_var_type = QtWidgets.QComboBox(Form)
        self.comboBox_var_type.setObjectName("comboBox_var_type")
        self.gridLayout.addWidget(self.comboBox_var_type, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_var_type.setText(_translate("Form", "变量类型"))
        self.label_var_name.setText(_translate("Form", "变量名称"))
        self.label_var_value.setText(_translate("Form", "变量值"))

