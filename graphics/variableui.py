# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-01 14:06:03
@Desc: 
"""

from PyQt5 import QtWidgets, QtGui
from ui.VariableWidget import Ui_Form
from data.variable import GetVariable


class CVariableWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CVariableWidget, self).__init__(parent)
        self.m_GloablVarUI = None
        self.InitUI()

    def InitUI(self):
        VBox = QtWidgets.QVBoxLayout(self)
        self.m_GloablVarUI = CGloablVariableUI("全局变量", GetVariable().GetAllVarInfo())
        self.m_GloablVarUI2 = CGloablVariableUI("局部变量", GetVariable().GetAllVarInfo())
        VBox.addWidget(self.m_GloablVarUI)
        VBox.addWidget(self.m_GloablVarUI2)
        self.setLayout(VBox)


class CGloablVariableUI(QtWidgets.QWidget, Ui_Form):
    def __init__(self, sName, dInfo, parent=None):
        super(CGloablVariableUI, self).__init__(parent)
        self.setupUi(self)
        self.m_Info = dInfo
        self.m_Name = sName
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.m_Name)
        self.treeWidget.headerItem().setText(0, self.m_Name)
        for sName, dTemp in self.m_Info.items():
            item = QtWidgets.QTreeWidgetItem(self.treeWidget)
            item.setText(0, sName)
            item.setText(1, sName + "_1")
            icon = QtGui.QIcon()
            iType = dTemp["type"]
            pix = ":/icon/btn_%s.png" % iType
            icon.addPixmap(QtGui.QPixmap(pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item.setIcon(0, icon)
