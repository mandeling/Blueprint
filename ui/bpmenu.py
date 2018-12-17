# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bpmenu.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_complie = QtWidgets.QPushButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/bp/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_complie.setIcon(icon)
        self.pushButton_complie.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_complie.setObjectName("pushButton_complie")
        self.horizontalLayout.addWidget(self.pushButton_complie)
        self.pushButton_start = QtWidgets.QPushButton(Form)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/bp/start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_start.setIcon(icon1)
        self.pushButton_start.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout.addWidget(self.pushButton_start)
        self.pushButton_debug = QtWidgets.QPushButton(Form)
        self.pushButton_debug.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/bp/debug.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_debug.setIcon(icon2)
        self.pushButton_debug.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_debug.setObjectName("pushButton_debug")
        self.horizontalLayout.addWidget(self.pushButton_debug)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.BPtabWidget = CBlueprintView(Form)
        self.BPtabWidget.setObjectName("BPtabWidget")
        self.verticalLayout.addWidget(self.BPtabWidget)

        self.retranslateUi(Form)
        self.BPtabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_complie.setText(_translate("Form", "编译"))
        self.pushButton_start.setText(_translate("Form", "开始"))
        self.pushButton_debug.setText(_translate("Form", "调试"))

from graphics.bptabwidget import CBlueprintView
from . import res_rc
