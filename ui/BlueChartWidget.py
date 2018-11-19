# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\mygithub\Blueprint\ui\BlueChartWidget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BlueChartWidget(object):
    def setupUi(self, BlueChartWidget):
        BlueChartWidget.setObjectName("BlueChartWidget")
        BlueChartWidget.resize(188, 107)
        BlueChartWidget.setStyleSheet("QWidget#BlueChartWidget{\n"
"background:transparent;\n"
"}\n"
"QWidget#BCWidget{\n"
"background:rgba(0, 0, 0, 200);\n"
"border-style:solid;\n"
"border-width:0px;\n"
"border-radius:10px;\n"
"}\n"
"QWidget#top{\n"
"border-style:solid;\n"
"border-width:0px;\n"
"background:qlineargradient(spread:pad, x1:0.00564972, y1:0.358, x2:1, y2:0.637, stop:0 rgba(0, 104, 183, 200), stop:1 rgba(0, 160, 233, 50));\n"
"border-top-left-radius:10px;\n"
"border-top-right-radius:10px;\n"
"border-bottom-left-radius:0px;\n"
"border-bottom-right-radius:0px;\n"
"}\n"
"QLabel{\n"
"color:white;\n"
"}\n"
"QPushButton{\n"
"background-color:transparent;\n"
"color:white;\n"
"border:none;\n"
"}\n"
"QPushButton:hover{\n"
"background:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(255, 0, 0, 0), stop:0.175141 rgba(255, 255, 255, 100), stop:0.824859 rgba(255, 255, 255, 100), stop:1 rgba(0, 0, 255, 0));\n"
"border-image:transparent;\n"
"color:white;\n"
"}\n"
"QWidget#outline{\n"
"background:transparent;\n"
"border:4px solid rgb(244, 100, 0);\n"
"border-radius:14px;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(BlueChartWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.BCWidget = QtWidgets.QWidget(BlueChartWidget)
        self.BCWidget.setObjectName("BCWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.BCWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.top = QtWidgets.QWidget(self.BCWidget)
        self.top.setObjectName("top")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.top)
        self.horizontalLayout_3.setContentsMargins(6, 2, 4, 2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lb_Title = QtWidgets.QLabel(self.top)
        self.lb_Title.setObjectName("lb_Title")
        self.horizontalLayout_3.addWidget(self.lb_Title)
        spacerItem = QtWidgets.QSpacerItem(67, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btn_ShowProperty = QtWidgets.QPushButton(self.top)
        self.btn_ShowProperty.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon_more.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_ShowProperty.setIcon(icon)
        self.btn_ShowProperty.setIconSize(QtCore.QSize(20, 20))
        self.btn_ShowProperty.setObjectName("btn_ShowProperty")
        self.horizontalLayout_3.addWidget(self.btn_ShowProperty)
        self.verticalLayout_2.addWidget(self.top)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_Input = QtWidgets.QPushButton(self.BCWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/btn_1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_Input.setIcon(icon1)
        self.btn_Input.setIconSize(QtCore.QSize(20, 20))
        self.btn_Input.setObjectName("btn_Input")
        self.horizontalLayout.addWidget(self.btn_Input)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btn_Start = QtWidgets.QPushButton(self.BCWidget)
        self.btn_Start.setLayoutDirection(QtCore.Qt.RightToLeft)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/btn_2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_Start.setIcon(icon2)
        self.btn_Start.setIconSize(QtCore.QSize(20, 20))
        self.btn_Start.setObjectName("btn_Start")
        self.horizontalLayout.addWidget(self.btn_Start)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_Source = QtWidgets.QPushButton(self.BCWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/btn_3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_Source.setIcon(icon3)
        self.btn_Source.setIconSize(QtCore.QSize(20, 20))
        self.btn_Source.setObjectName("btn_Source")
        self.horizontalLayout_2.addWidget(self.btn_Source)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.btn_End = QtWidgets.QPushButton(self.BCWidget)
        self.btn_End.setLayoutDirection(QtCore.Qt.RightToLeft)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/btn_4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_End.setIcon(icon4)
        self.btn_End.setIconSize(QtCore.QSize(20, 20))
        self.btn_End.setObjectName("btn_End")
        self.horizontalLayout_2.addWidget(self.btn_End)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addWidget(self.BCWidget)

        self.retranslateUi(BlueChartWidget)
        QtCore.QMetaObject.connectSlotsByName(BlueChartWidget)

    def retranslateUi(self, BlueChartWidget):
        _translate = QtCore.QCoreApplication.translate
        BlueChartWidget.setWindowTitle(_translate("BlueChartWidget", "Form"))
        self.lb_Title.setText(_translate("BlueChartWidget", "TextLabel"))
        self.btn_Input.setText(_translate("BlueChartWidget", "in"))
        self.btn_Start.setText(_translate("BlueChartWidget", "start"))
        self.btn_Source.setText(_translate("BlueChartWidget", "资源"))
        self.btn_End.setText(_translate("BlueChartWidget", "end"))

import res_rc
