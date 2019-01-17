# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-17 15:14:03
@Desc: 引脚子控件
"""

from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import QSize

import bpdata.define as bddefine
from editdata import interface
from signalmgr import GetSignal


LINEEDIT_STYLESHEET = """
QLineEdit{
    background:transparent;
    border:1px solid #e6e6e6;
    color:white;
}
QLineEdit::focus{
    border-color:#0078d7
}
"""


class CValidatorLineEdit(QLineEdit):
    def __init__(self, pinID, iDataType, parent=None):
        super(CValidatorLineEdit, self).__init__(parent)
        self.m_PinID = pinID
        self.m_DataType = iDataType
        self.m_LastVar = None
        self._InitUI()
        self._InitSignal()

    def _InitUI(self):
        self.setStyleSheet(LINEEDIT_STYLESHEET)
        self.setMinimumSize(QSize(40, 20))
        if self.m_DataType == bddefine.Type.INT:
            self.setValidator(QIntValidator())
        elif self.m_DataType == bddefine.Type.FLOAT:
            self.setValidator(QDoubleValidator())
        value = interface.GetPinAttr(self.m_PinID, bddefine.PinAttrName.VALUE)
        self.setText(str(value))
        self.m_LastVar = value

    def _InitSignal(self):
        self.editingFinished.connect(self.S_EditingFinished)

    def S_EditingFinished(self):
        text = self.text()
        if not text and self.m_DataType in (bddefine.Type.INT, bddefine.Type.FLOAT):
            text = "0"
        value, bSuc = bddefine.ForceTransValue(bddefine.Type.INT, text)
        if not bSuc:
            return
        if value == self.m_LastVar:
            return
        self.m_LastVar = value
        interface.SetPinAttr(self.m_PinID, bddefine.PinAttrName.VALUE, value)
