# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-14 11:04:55
@Desc: 
"""

from PyQt5 import QtWidgets
from ui import VariableDetail
from editdata import interface
from editdata import define as eddefine
from bpdata import define as bddefine
from signalmgr import GetSignal


class CDetailUI(QtWidgets.QWidget):
    def __init__(self, bpID, parent=None):
        super(CDetailUI, self).__init__(parent)
        self.m_BPID = bpID
        self._InitUI()
        self._InitSignal()
        self.m_CurName = ""
        self.m_CurType = None
        self.m_CurValue = None
        self.m_VarID = None

    def _InitUI(self):
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.m_VariableDetail = CVariableDetail(self)
        spacerItem = QtWidgets.QSpacerItem(20, 940, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addWidget(self.m_VariableDetail)
        self.verticalLayout.addItem(spacerItem)
        for sName in bddefine.NAME_TYPE:
            self.m_VariableDetail.comboBox_var_type.addItem(sName)

    def _InitSignal(self):
        GetSignal().UI_OPEN_VARIABLE_DETAIL.connect(self.S_OpenVariable)
        self.m_VariableDetail.lineEdit_var_name.editingFinished.connect(self.S_NameEditingFinished)
        self.m_VariableDetail.lineEdit_var_value.editingFinished.connect(self.S_ValueEditingFinished)
        self.m_VariableDetail.comboBox_var_type.currentIndexChanged.connect(self.S_TypeChanged)

    def S_OpenVariable(self, bpID, varID):
        if bpID != self.m_BPID:
            return
        iType = interface.GetVariableAttr(varID, eddefine.VariableAttrName.TYPE)
        value = interface.GetVariableAttr(varID, eddefine.VariableAttrName.VALUE)
        sName = interface.GetVariableAttr(varID, eddefine.VariableAttrName.NAME)
        self.m_VariableDetail.lineEdit_var_name.setText(sName)
        self.m_VariableDetail.lineEdit_var_value.setText(str(value))
        sType = bddefine.TYPE_NAME[iType]
        self.m_VariableDetail.comboBox_var_type.setCurrentText(sType)
        self.m_CurName = sName
        self.m_CurType = iType
        self.m_CurValue = value
        self.m_VarID = varID

    def S_NameEditingFinished(self):
        sName = self.m_VariableDetail.lineEdit_var_name.text()
        if sName == self.m_CurName:
            return
        GetSignal().UI_VARIABLE_CHANGE_ATTR.emit(self.m_VarID, eddefine.VariableAttrName.NAME, sName)
        self.m_CurName = sName

    def S_ValueEditingFinished(self):
        sValue = self.m_VariableDetail.lineEdit_var_value.text()
        value, bSuc = bddefine.ForceTransValue(self.m_CurType, sValue)
        if not bSuc or value == self.m_CurValue:
            return
        GetSignal().UI_VARIABLE_CHANGE_ATTR.emit(self.m_VarID, eddefine.VariableAttrName.VALUE, value)
        self.m_CurValue = value

    def S_TypeChanged(self):
        sType = self.m_VariableDetail.comboBox_var_type.currentText()
        iType = bddefine.NAME_TYPE[sType]
        if iType == self.m_CurType:
            return
        value = bddefine.GetDefauleValue(iType)
        GetSignal().UI_VARIABLE_CHANGE_ATTR.emit(self.m_VarID, eddefine.VariableAttrName.TYPE, iType)
        self.m_VariableDetail.lineEdit_var_value.setText(str(value))
        self.m_CurType = iType


class CVariableDetail(QtWidgets.QWidget, VariableDetail.Ui_Form):
    def __init__(self, parent=None):
        super(CVariableDetail, self).__init__(parent)
        self.setupUi(self)
