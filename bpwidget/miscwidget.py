# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-14 15:49:33
@Desc: 
"""

import uisignal
from PyQt5 import QtWidgets
from editdata import interface
from editdata import define as eddefine


class CTreeWidget(QtWidgets.QTreeWidget):
    def mousePressEvent(self, event):
        super(CTreeWidget, self).mousePressEvent(event)
        oItem = self.currentItem()
        sName = oItem.text(0)
        uisignal.GetSignal().VARIABLE_OPEN.emit(sName)

    def closeEditor(self, oLine, iIndex):
        super(CTreeWidget, self).closeEditor(oLine, iIndex)
        oItem = self.currentItem()
        newName = oLine.text()
        oldName = oItem.GetName()
        if oldName == newName:
            return
        uisignal.GetSignal().VARIABLE_CHANGE_NAME.emit(oldName, newName)
