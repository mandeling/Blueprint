# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-14 11:04:55
@Desc: 
"""

import uisignal

from PyQt5 import QtWidgets
from ui import VariableDetail
from editdata import interface
from editdata import define as eddefine
from bpdata import define as bddefine


class CDetailUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CDetailUI, self).__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.m_VariableDetail = CVariableDetail(self)
        spacerItem = QtWidgets.QSpacerItem(20, 940, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addWidget(self.m_VariableDetail)
        self.verticalLayout.addItem(spacerItem)
        self.m_CurName = ""
        self.m_CurType = None
        self.m_CurValue = None
        self.m_IsOpen = False
        self.InitUI()
        self.InitSingal()

    def InitSingal(self):
        uisignal.GetSignal().VARIABLE_OPEN.connect(self.S_OpenVariable)
        self.m_VariableDetail.lineEdit_var_name.editingFinished.connect(self.S_NameEditingFinished)
        self.m_VariableDetail.lineEdit_var_value.editingFinished.connect(self.S_ValueEditingFinished)
        self.m_VariableDetail.comboBox_var_type.currentIndexChanged.connect(self.S_TypeChanged)

    def InitUI(self):
        for sName in bddefine.NAME_TYPE:
            self.m_VariableDetail.comboBox_var_type.addItem(sName)

    def S_OpenVariable(self, sName):
        self.m_IsOpen = True
        iType = interface.GetVariableAttr(sName, eddefine.VariableAttrName.TYPE)
        value = interface.GetVariableAttr(sName, eddefine.VariableAttrName.VALUE)
        self.m_VariableDetail.lineEdit_var_name.setText(sName)
        self.m_VariableDetail.lineEdit_var_value.setText(str(value))
        sType = bddefine.TYPE_NAME[iType]
        self.m_VariableDetail.comboBox_var_type.setCurrentText(sType)
        self.m_CurName = sName
        self.m_CurType = iType
        self.m_CurValue = value
        self.m_IsOpen = False

    def S_NameEditingFinished(self):
        sName = self.m_VariableDetail.lineEdit_var_name.text()
        if sName == self.m_CurName:
            return
        print("S_NameEditingFinished", sName, self.m_CurName)
        self.m_VariableDetail.lineEdit_var_name.setText(sName)
        uisignal.GetSignal().VARIABLE_CHANGE_NAME.emit(self.m_CurName, sName)
        self.m_CurName = sName

    def S_ValueEditingFinished(self):
        sValue = self.m_VariableDetail.lineEdit_var_value.text()
        value, bSuc = bddefine.ForceTransValue(self.m_CurType, sValue)
        print("S_ValueEditingFinished", sValue, self.m_CurValue)
        if bSuc:
            interface.SetVariableAttr(self.m_CurName, eddefine.VariableAttrName.VALUE, value)
            self.m_CurValue = value
            return
        self.m_VariableDetail.lineEdit_var_value.setText(str(value))
        self.m_CurValue = value

    def S_TypeChanged(self):
        if self.m_IsOpen:
            return
        sType = self.m_VariableDetail.comboBox_var_type.currentText()
        iType = bddefine.NAME_TYPE[sType]
        value = bddefine.GetDefauleValue(iType)
        self.m_VariableDetail.lineEdit_var_value.setText(str(value))
        print("S_TypeChanged", iType, self.m_CurType)
        self.m_CurType = iType
        uisignal.GetSignal().VARIABLE_CHANGE_TYPE.emit(self.m_CurName, iType)


class CVariableDetail(QtWidgets.QWidget, VariableDetail.Ui_Form):
    def __init__(self, parent=None):
        super(CVariableDetail, self).__init__(parent)
        self.setupUi(self)
