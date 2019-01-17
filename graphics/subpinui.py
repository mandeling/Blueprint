# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-17 15:14:03
@Desc: 引脚子控件
"""

from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QCheckBox
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import QSize, Qt

import bpdata.define as bddefine
from editdata import interface


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
        self._InitData()

    def _InitUI(self):
        self.setStyleSheet(LINEEDIT_STYLESHEET)
        self.setMinimumSize(QSize(40, 20))
        if self.m_DataType == bddefine.Type.INT:
            self.setValidator(QIntValidator())
        elif self.m_DataType == bddefine.Type.FLOAT:
            self.setValidator(QDoubleValidator())
        self.setText("")
        self.setFixedSize(20, 20)

    def _InitData(self):
        value = interface.GetPinAttr(self.m_PinID, bddefine.PinAttrName.VALUE)
        self.setText(str(value))
        self.m_LastVar = value

    def _InitSignal(self):
        self.textChanged.connect(self.S_TextChanged)
        self.editingFinished.connect(self.S_EditingFinished)

    def S_TextChanged(self):
        text = self.text()
        qTextRect = self.fontMetrics().boundingRect(text)
        w = qTextRect.width() + 20
        h = self.height()
        w = 20 if w < 20 else w
        h = 20 if h < 20 else h
        if not text:
            w = 20
        self.setFixedSize(w, h)
        parentWidget = self.parent()
        while parentWidget:
            parentWidget.adjustSize()
            parentWidget = parentWidget.parent()

    def S_EditingFinished(self):
        text = self.text()
        if not text and self.m_DataType in (bddefine.Type.INT, bddefine.Type.FLOAT):
            text = "0"
        value, bSuc = bddefine.ForceTransValue(bddefine.Type.INT, text)
        if not bSuc:
            return
        if value == self.m_LastVar:
            return
        interface.SetPinAttr(self.m_PinID, bddefine.PinAttrName.VALUE, value)
        self.m_LastVar = value
        self.setText(str(value))
        self.clearFocus()


class CCheckBox(QCheckBox):
    def __init__(self, pinID, parent=None):
        super(CCheckBox, self).__init__(parent)
        self.m_PinID = pinID
        self.m_LastVar = None
        self._InitUI()
        self._InitSignal()
        self._InitData()

    def _InitUI(self):
        size = QSize(20, 20)
        self.setMinimumSize(size)
        self.setMaximumSize(size)

    def _InitSignal(self):
        self.toggled.connect(self.S_CheckedChanged)

    def _InitData(self):
        value = interface.GetPinAttr(self.m_PinID, bddefine.PinAttrName.VALUE)
        if value:
            self.setCheckState(Qt.Checked)
        else:
            self.setCheckState(Qt.Unchecked)
        self.m_LastVar = value

    def S_CheckedChanged(self, value):
        if value == self.m_LastVar:
            return
        interface.SetPinAttr(self.m_PinID, bddefine.PinAttrName.VALUE, value)
        self.m_LastVar = value
