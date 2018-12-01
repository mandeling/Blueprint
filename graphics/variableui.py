# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-01 14:06:03
@Desc: 
"""

from PyQt5 import QtWidgets, QtGui
from ui.VariableWidget import Ui_Form

TESTINGO = {
    "test1": 1,
    "test2": 2,
    "test3": 3,
    "test4": 4,
    "test5": 5,
    "test6": 6,
    "test7": 7,
    "test8": 8,
    "test9": 9,
    "test10": 10,
}


class CVariableUI(QtWidgets.QWidget, Ui_Form):
    def __init__(self, sName, dInfo, parent=None):
        super(CVariableUI, self).__init__(parent)
        self.setupUi(self)
        self.m_Info = dInfo
        self.m_Name = sName
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.m_Name)
        self.treeWidget.headerItem().setText(0, self.m_Name)
        for sName, iType in self.m_Info.items():
            item = QtWidgets.QTreeWidgetItem(self.treeWidget)
            item.setText(0, sName)
            item.setText(1, sName + "_1")
            icon = QtGui.QIcon()
            pix = ":/icon/btn_%s.png" % iType
            icon.addPixmap(QtGui.QPixmap(pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item.setIcon(0, icon)
