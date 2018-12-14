# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-01 14:06:03
@Desc: 
"""
import signal

from PyQt5 import QtWidgets, QtGui, QtCore
from ui.VariableWidget import Ui_Form

from editdata import interface
from bpdata import define as bddefine
from editdata import define as eddefine


class CVariableWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CVariableWidget, self).__init__(parent)
        self.m_GloablVarUI = None
        self.InitUI()

    def InitUI(self):
        VBox = QtWidgets.QVBoxLayout(self)
        self.m_GloablVarUI = CGloablVariableUI("全局变量", interface.GetVariableData())
        self.m_GloablVarUI2 = CGloablVariableUI("局部变量", interface.GetVariableData())
        VBox.addWidget(self.m_GloablVarUI)
        VBox.addWidget(self.m_GloablVarUI2)
        self.setLayout(VBox)


class CGloablVariableUI(QtWidgets.QWidget, Ui_Form):
    def __init__(self, sName, dInfo, parent=None):
        super(CGloablVariableUI, self).__init__(parent)
        self.setupUi(self)
        self.m_Info = dInfo
        self.m_ID = 0
        self.m_Name = sName
        self.InitUI()
        self.InitConnect()

    def InitConnect(self):
        self.pushButton_add.clicked.connect(self.S_NewVariable)

    def InitUI(self):
        self.setWindowTitle(self.m_Name)
        self.treeWidget.headerItem().setText(0, self.m_Name)
        for sName, dTemp in self.m_Info.items():
            iType = interface.GetVariableAttr(sName, eddefine.VariableAttrName.TYPE)
            CTreeWidgetItem(sName, iType, self.treeWidget)

    def S_NewVariable(self):
        self.m_ID += 1
        sName = "NewVar_%s" % self.m_ID
        iType = bddefine.Type.INT
        interface.NewVariable(sName, iType)
        CTreeWidgetItem(sName, iType, self.treeWidget)
        signal.GetSignal().VARIABLE_OPEN.emit(sName)


class CTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, sName, iType=bddefine.Type.INT, parent=None):
        super(CTreeWidgetItem, self).__init__(parent)
        self.m_Name = sName
        self.m_Type = iType  # 变量类型
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
        self.SetMyName()
        self.SetMyIcon()

    def SetMyName(self, sName=None):
        if sName:
            self.m_Name = sName
        self.setText(0, self.m_Name)

    def SetMyIcon(self, iType=None):
        if iType is not None:
            self.m_Type = iType
        icon = QtGui.QIcon()
        pix = ":/icon/btn_%s.png" % self.m_Type
        icon.addPixmap(QtGui.QPixmap(pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(0, icon)
