# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-17 15:14:03
@Desc: 引脚子控件
"""

from PyQt5.QtWidgets import QWidget, QLineEdit, QCheckBox, QLabel, QComboBox,\
    QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
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


class CBaseLineEdit(QLineEdit):
    def __init__(self, iDataType, parent=None):
        super(CBaseLineEdit, self).__init__(parent)
        self.m_DataType = iDataType
        self._InitUI()
        self._InitSignal()

    def _InitUI(self):
        self.setStyleSheet(LINEEDIT_STYLESHEET)
        self.setMinimumSize(QSize(40, 20))
        if self.m_DataType == bddefine.Type.INT:
            self.setValidator(QIntValidator())
        elif self.m_DataType == bddefine.Type.FLOAT:
            self.setValidator(QDoubleValidator())
        self.setText("")
        self.setFixedSize(20, 20)

    def _InitSignal(self):
        self.textChanged.connect(self.S_TextChanged)

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


class CValidatorLineEdit(CBaseLineEdit):
    def __init__(self, pinID, iDataType, parent=None):
        super(CValidatorLineEdit, self).__init__(iDataType, parent)
        self.m_PinID = pinID
        self.m_LastVar = None
        self._InitData()

    def _InitData(self):
        value = interface.GetPinAttr(self.m_PinID, bddefine.PinAttrName.VALUE)
        self.setText(str(value))
        self.m_LastVar = value

    def _InitSignal(self):
        super(CValidatorLineEdit, self)._InitSignal()
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


class CEnum(QWidget):
    def __init__(self, pinID, parent=None):
        super(CEnum, self).__init__(parent)
        self.m_PinID = pinID
        self.m_EnumBox = None
        self.m_ValueBox = None
        self.m_Test = {
            "Enum1": ["1", "2", "3", "4"],
            "Enum2": ["11", "22", "33"],
            "Enum3": ["111", "222", "333", "444", "555"],
        }
        self._InitUI()
        self._InitSignal()
        self._InitData()

    def _InitUI(self):
        vBox = QVBoxLayout(self)
        hBox1 = QHBoxLayout()
        lable1 = QLabel("枚举", self)
        self.m_EnumBox = QComboBox(self)
        hBox1.addWidget(lable1)
        hBox1.addWidget(self.m_EnumBox)
        hBox2 = QHBoxLayout()
        lable2 = QLabel("值", self)
        self.m_ValueBox = QComboBox(self)
        hBox2.addWidget(lable2)
        hBox2.addWidget(self.m_ValueBox)
        vBox.addLayout(hBox1)
        vBox.addLayout(hBox2)

    def _InitSignal(self):
        self.m_EnumBox.currentTextChanged.connect(self.S_EnumTypeChange)
        self.m_ValueBox.currentTextChanged.connect(self.S_ValueTypeChange)

    def _InitData(self):
        for sEnum in self.m_Test:
            self.m_EnumBox.addItem(sEnum)
        self.m_ValueBox.setCurrentIndex(0)

    def S_EnumTypeChange(self, sText):
        print("EnumType", sText)
        lst = self.m_Test[sText]
        self.m_ValueBox.clear()
        self.m_ValueBox.addItems(lst)
        self.m_ValueBox.setCurrentIndex(-1)

    def S_ValueTypeChange(self, sText):
        print("ValueType", sText)


class CVector3(QWidget):
    m_Num = 3

    def __init__(self, pinID, parent=None):
        super(CVector3, self).__init__(parent)
        self.m_PinID = pinID
        self.m_LineList = []
        self._InitUI()
        self._InitData()

    def _InitUI(self):
        hBox = QHBoxLayout(self)
        for i in range(self.m_Num):
            oLine = CBaseLineEdit(bddefine.Type.FLOAT, self)
            hBox.addWidget(oLine)
            self.m_LineList.append(oLine)
            oLine.editingFinished.connect(self.S_EditingFinished)

    def _InitData(self):
        vct = (0, 0, 0)
        for i, value in enumerate(vct):
            oLine = self.m_LineList[i]
            oLine.setText(str(value))

    def S_EditingFinished(self):
        vct = [0, 0, 0]
        for i, oLine in enumerate(self.m_LineList):
            sValue = oLine.text()
            value, bSuc = bddefine.ForceTransValue(bddefine.Type.FLOAT, sValue)
            if bSuc:
                vct[i] = value
        print("Vector3:", vct)


class CComCheckBox(QWidget):
    def __init__(self, pinID, parent=None):
        super(CComCheckBox, self).__init__(parent)
        self.m_PinID = pinID
        self.m_List = ["132434", "2", "3", "4"]
        self.m_Select = []
        self.m_ComBox = QComboBox(self)
        self.m_LineEdit = None
        self._InitUI()

    def _InitUI(self):
        self.setMinimumSize(QSize(100, 80))
        listWidget = QListWidget(self)
        lineEdit = QLineEdit(self)
        for i, txt in enumerate(self.m_List):
            item = QListWidgetItem(listWidget)
            listWidget.addItem(item)
            item.setData(Qt.UserRole, i)
            checkbox = QCheckBox(self)
            checkbox.setText(txt)
            listWidget.addItem(item)
            listWidget.setItemWidget(item, checkbox)
            checkbox.toggled.connect(self.S_StateChanged)

        self.m_ComBox.setModel(listWidget.model())
        self.m_ComBox.setView(listWidget)
        self.m_ComBox.setLineEdit(lineEdit)
        lineEdit.setReadOnly(True)

        hbox = QVBoxLayout(self)
        hbox.addWidget(self.m_ComBox)

        self.m_LineEdit = lineEdit

    def S_StateChanged(self, value):
        checkbox = self.sender()
        txt = checkbox.text()
        if value:
            self.m_Select.append(txt)
        else:
            self.m_Select.remove(txt)
        sLine = "&".join(self.m_Select)
        self.m_LineEdit.setText(sLine)
