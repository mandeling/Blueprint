# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-10 10:04:07
@Desc: 搜索窗口
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,\
    QLineEdit, QPushButton, QFrame, QTreeView, QAbstractItemView
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from signalmgr import GetSignal
from editdata import interface
from . import define

import editdata.define as eddefine
import bpdata.define as bddefine


class CSearchWidget(QWidget):
    def __init__(self, bpID, parent=None):
        super(CSearchWidget, self).__init__(parent)
        self.m_BPID = bpID
        self.m_Status = define.FULL_MATCH
        self.m_Search = None
        self.m_CaseSensitively = None
        self.m_WholeWords = None
        self.m_Regular = None
        self.m_Tree = None
        self._InitUI()
        self._InitSignal()

    def _InitUI(self):
        self.setWindowTitle("搜索")
        vBox = QVBoxLayout(self)
        hBox = QHBoxLayout(self)
        self.m_Search = QLineEdit(self)
        self.m_Search.setFocusPolicy(Qt.ClickFocus)
        self.m_Search.setClearButtonEnabled(True)
        hBox.addWidget(self.m_Search)

        self.m_BtnMatch = QPushButton("全匹配", self)
        self.m_BtnMatch.setToolTip("点击切换全匹配/模糊匹配")
        hBox.addWidget(self.m_BtnMatch)

        vBox.addLayout(hBox)

        line = QFrame(self)
        line.setMinimumSize(QSize(0, 2))
        line.setMaximumSize(QSize(1234567, 2))
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        vBox.addWidget(line)

        self.m_Tree = QTreeView(self)
        self.m_Tree.setHeaderHidden(True)
        self.m_Tree.setModel(QStandardItemModel(self))
        self.m_Tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        vBox.addWidget(self.m_Tree)
        self.setLayout(vBox)

    def _InitSignal(self):
        self.m_BtnMatch.clicked.connect(self.S_ChangeMatch)
        self.m_Search.returnPressed.connect(self.S_Search)
        self.m_Tree.doubleClicked.connect(self.S_FocusItem)
        GetSignal().UI_SHOW_BP_SEARCH.connect(self.S_ShowBPSearch)

    def S_ChangeMatch(self):
        self.m_Status ^= define.FUZZY_MATCH
        if self.m_Status & define.FUZZY_MATCH:
            self.m_BtnMatch.setText("模糊匹配")
        else:
            self.m_BtnMatch.setText("全匹配")

    def S_ShowBPSearch(self, bpID):
        if bpID == self.m_BPID:
            self.show()

    def S_Search(self):
        sText = self.m_Search.text()
        if not sText:
            return
        dInfo = interface.GetSearchInfo(self.m_BPID, sText, self.m_Status & define.FUZZY_MATCH)
        parentModel = self.m_Tree.model()
        parentModel.clear()
        for graphicID, dNode in dInfo.items():
            graphicName = interface.GetGraphicAttr(graphicID, eddefine.GraphicAttrName.NAME)
            tInfo = (define.SearchTreeItemType.GRAPHIC, graphicID)
            oGItem = CStandardItem(graphicName, tInfo)
            parentModel.appendRow(oGItem)
            for nodeID, lstPin in dNode.items():
                nodeName = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.DISPLAYNAME)
                tInfo = (define.SearchTreeItemType.NODE, nodeID)
                oNItem = CStandardItem(nodeName, tInfo)
                oGItem.appendRow(oNItem)
                for pinID in lstPin:
                    pinName = interface.GetPinAttr(pinID, bddefine.PinAttrName.DISPLAYNAME)
                    tInfo = (define.SearchTreeItemType.PIN, pinID)
                    oPItem = CStandardItem(pinName, tInfo)
                    oNItem.appendRow(oPItem)
        self.m_Tree.expandAll()

    def S_FocusItem(self, oModelIndex):
        """
        oModelIndex QModelIndex
        self.model() QStandardItemModel
        """
        item = self.m_Tree.model().itemFromIndex(oModelIndex)
        if not item:
            return
        iItemType, ID = item.GetInfo()
        if iItemType == define.SearchTreeItemType.GRAPHIC:
            GetSignal().UI_FOCUS_GRAPHIC.emit(self.m_BPID, ID)
        else:
            if iItemType == define.SearchTreeItemType.PIN:
                ID = interface.GetNodeIDByPinID(ID)
            graphicID = interface.GetGraphicIDByNodeID(ID)
            GetSignal().UI_FOCUS_GRAPHIC.emit(self.m_BPID, graphicID)
            GetSignal().UI_FOCUS_NODE.emit(graphicID, ID)


class CStandardItem(QStandardItem):
    def __init__(self, sName, tInfo):
        super(CStandardItem, self).__init__(sName)
        self.m_Info = tInfo

    def GetInfo(self):
        return self.m_Info
