# -*- coding:utf-8 -*-
'''
@Description: 项目的QLineEdit
@Author: lamborghini1993
@Date: 2019-03-13 11:43:30
@UpdateDate: 2019-03-13 14:15:21
'''

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import QSize

import bpdata.define as bddefine


class CTypeLineEdit(QLineEdit):
    """
    限制输入内容的QLineEdit
    """

    def __init__(self, iDataType, parent=None):
        super(CTypeLineEdit, self).__init__(parent)
        self.m_DataType = iDataType
        self._InitUI()

    def _InitUI(self):
        if self.m_DataType == bddefine.Type.INT:
            self.setValidator(QIntValidator())
            self.setText("0")
        elif self.m_DataType == bddefine.Type.FLOAT:
            self.setValidator(QDoubleValidator())
            self.setText("0.0")
        else:
            self.setText("")


class CCVariableLengthTypeLineEdit(CTypeLineEdit):
    """
    可变长度+限制输入内容的QLineEdit
    """
    m_MinNum = 20

    def __init__(self, iDataType, parent=None):
        super(CCVariableLengthTypeLineEdit).__init__(iDataType, parent)
        self._InitSignal()

    def _InitUI(self):
        super(CCVariableLengthTypeLineEdit, self)._InitUI()
        self.setMinimumSize(QSize(40, self.m_MinNum))
        self.setFixedSize(self.m_MinNum, self.m_MinNum)

    def _InitSignal(self):
        self.textChanged.connect(self.S_TextChanged)

    def S_TextChanged(self):
        text = self.text()
        qTextRect = self.fontMetrics().boundingRect(text)
        w = qTextRect.width() + self.m_MinNum
        h = self.height()
        w = self.m_MinNum if w < self.m_MinNum else w
        h = self.m_MinNum if h < self.m_MinNum else h
        if not text:
            w = self.m_MinNum
        self.setFixedSize(w, h)
        parentWidget = self.parent()
        while parentWidget:
            parentWidget.adjustSize()
            parentWidget = parentWidget.parent()
