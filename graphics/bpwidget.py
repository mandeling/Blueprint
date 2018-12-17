# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-17 16:28:34
@Desc: 蓝图widget
"""

from ui import bpmenu
from PyQt5 import QtWidgets


class CBlueprintWidget(QtWidgets.QWidget, bpmenu.Ui_Form):
    def __init__(self, parent=None):
        super(CBlueprintWidget, self).__init__(parent)
        self.setupUi(self)

    def NewBlueprint(self):
        self.BPtabWidget.AddBlueprint()

    def SaveBlueprint(self):
        self.BPtabWidget.SaveBlueprint()

    def OpenBlueprint(self):
        self.BPtabWidget.OpenBlueprint()
