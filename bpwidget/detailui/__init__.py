# -*- coding:utf-8 -*-
'''
@Description: 细节UI
@Author: lamborghini1993
@Date: 2019-02-27 11:29:52
@UpdateDate: 2019-02-27 14:51:22
'''

from PyQt5 import QtWidgets
from signalmgr import GetSignal
from viewmgr.uimgr import GetUIMgr
from . import varwidget


class CDetailUI(QtWidgets.QWidget):
    def __init__(self, bpID, parent=None):
        super(CDetailUI, self).__init__(parent)
        self.m_BPID = bpID
        self.m_Box = QtWidgets.QVBoxLayout(self)
        self.m_DetaiWidget = None
        GetUIMgr().AddDetailUI(self.m_BPID, self)

    def __del__(self):
        GetUIMgr().DelDetailUI(self.m_BPID)

    def _RemoveWidget(self):
        if not self.m_DetaiWidget:
            return
        self.m_DetaiWidget.setParent(None)
        index = self.m_Box.indexOf(self.m_DetaiWidget)
        item = self.m_Box.itemAt(index)
        self.m_Box.removeWidget(self.m_DetaiWidget)
        self.m_Box.removeItem(item)
        self.m_DetaiWidget = None
        self.adjustSize()

    def SetVarWidget(self, varID):
        self._RemoveWidget()
        self.m_DetaiWidget =varwidget.CVarWidget(varID)
        self.m_Box.addWidget(self.m_DetaiWidget)
        self.adjustSize()
