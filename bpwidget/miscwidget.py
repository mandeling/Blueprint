# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-14 15:49:33
@Desc: 
"""

import signal
from PyQt5 import QtWidgets


class CTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(CTreeWidget, self).__init__(parent)

    def mousePressEvent(self, event):
        super(CTreeWidget, self).mousePressEvent(event)
        oItem = self.currentItem()
        sName = oItem.text(0)
        signal.GetSignal().VARIABLE_OPEN.emit(sName)
