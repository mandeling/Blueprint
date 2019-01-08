# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-08 14:27:14
@Desc: 蓝图属性界面
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from . import variableui

class CBPAttrWidget(QWidget):
    def __init__(self, parent=None):
        super(CBPAttrWidget, self).__init__(parent)
        self._InitUI()

    def _InitUI(self):
        vBox = QVBoxLayout(self)
        vBox.addWidget(variableui.CVariableUI(self))
