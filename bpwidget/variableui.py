# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-01 14:06:03
@Desc: 
"""
import uisignal

from PyQt5 import QtWidgets, QtGui, QtCore
from ui.VariableWidget import Ui_Form

from editdata import interface
from bpdata import define as bddefine
from editdata import define as eddefine
from . import define


class CVariableUI(QtWidgets.QWidget, Ui_Form):
    m_Name = define.BP_ATTR_VARIABLE

    def __init__(self, bpID, parent=None):
        super(CVariableUI, self).__init__(parent)
        self.setupUi(self)
        self.m_BPID = bpID
        self.m_ID = 0
        self.m_ItemInfo = {}
        self.InitUI()
        # self.InitConnect()

    def InitConnect(self):
        self.pushButton_add.clicked.connect(self.S_NewVariable)
        uisignal.GetSignal().VARIABLE_CHANGE_NAME.connect(self.S_VariableChangeName)
        uisignal.GetSignal().VARIABLE_CHANGE_TYPE.connect(self.S_VariableChangeType)

    def InitUI(self):
        self.setWindowTitle(self.m_Name)
        self.treeWidget.headerItem().setText(0, self.m_Name)
        lstVar = interface.GetBlueprintAttr(self.m_BPID, eddefine.BlueprintAttrName.VARIABLE_LIST)
        for varID in lstVar:
            self.m_ItemInfo[varID] = CTreeWidgetItem(varID, self.treeWidget)

    def S_NewVariable(self):
        self.m_ID += 1
        sName = "NewVar_%s" % self.m_ID
        iType = bddefine.Type.INT
        interface.NewVariable()
        self.m_ItemInfo[sName] = CTreeWidgetItem(sName, iType, self.treeWidget)
        uisignal.GetSignal().VARIABLE_OPEN.emit(sName)

    def S_VariableChangeType(self, sName, iType):
        oItem = self.m_ItemInfo[sName]
        oItem.SetMyIcon(iType)
        interface.SetVariableAttr(sName, eddefine.VariableAttrName.TYPE, iType)

    def S_VariableChangeName(self, sOldName, sNewName):
        if sOldName == sNewName:
            return
        interface.SetVariableAttr(sOldName, eddefine.VariableAttrName.NAME, sNewName)
        oItem = self.m_ItemInfo[sOldName]
        oItem.SetMyName(sNewName)
        self.m_ItemInfo[sNewName] = oItem
        del self.m_ItemInfo[sOldName]
        uisignal.GetSignal().VARIABLE_OPEN.emit(sNewName)


class CTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, varID, parent=None):
        super(CTreeWidgetItem, self).__init__(parent)
        self.m_VarID = varID
        self.m_Name = interface.GetVariableAttr(varID, eddefine.VariableAttrName.NAME)
        self.m_Type = interface.GetVariableAttr(varID, eddefine.VariableAttrName.TYPE)
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

    def GetName(self):
        return self.m_Name

    def GetType(self):
        return self.m_Type
