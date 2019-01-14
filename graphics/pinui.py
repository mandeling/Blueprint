# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-14 14:58:39
@Desc: 节点槽UI
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QSizePolicy, QMenu
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QCursor

import bpdata.define as bddefine
from editdata import interface
from viewmgr.uimgr import GetUIMgr
from pubcode import functor


class CPinUI(QWidget):
    def __init__(self, pinID, parent=None):
        super(CPinUI, self).__init__(parent)
        self.m_PinID = pinID
        self.m_Btn = None
        self.m_Label = None
        self.m_HLayout = None
        self.m_Widget = None
        self._InitUI()
        self.SetIcon()
        self.SetText()
        GetUIMgr().AddPinUI(pinID, self)

    def __del__(self):
        GetUIMgr().DelPinUI(self.m_PinID)

    def _InitUI(self):
        hBox = QHBoxLayout(self)
        hBox.setContentsMargins(0, 0, 0, 0)
        hBox.setSpacing(6)
        self.m_Btn = CTypeButton(self.m_PinID, self)
        self.m_Label = QLabel(self)
        self.m_HLayout = QHBoxLayout()
        self.m_HLayout.setContentsMargins(0, 0, 0, 0)
        self.m_HLayout.setSpacing(6)
        hBox.addWidget(self.m_Btn)
        hBox.addWidget(self.m_Label)
        hBox.addLayout(self.m_HLayout)

    def contextMenuEvent(self, _):
        lstLineID = interface.GetAllLineByPin(self.m_PinID)
        if not lstLineID:
            return
        menu = QMenu()
        for lineID in lstLineID:
            oPinID = interface.GetLineOtherPin(lineID, self.m_PinID)
            sPinDisplayName = interface.GetPinAttr(oPinID, bddefine.PinAttrName.DISPLAYNAME)
            nodeID = interface.GetNodeIDByPinID(oPinID)
            sNodeDisplayName = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.DISPLAYNAME)
            sMsg = "删除与\"%s\"-\"%s\"的连线" % (sNodeDisplayName, sPinDisplayName)
            func = functor.Functor(self.scene().OnDelLineUI, lineID)
            menu.addAction(sMsg, func)
        menu.exec_(QCursor.pos())

    def SetIcon(self, iDataType=None):
        if iDataType is None:
            iPinType = interface.GetPinAttr(self.m_PinID, bddefine.PinAttrName.PIN_TYPE)
            if bddefine.PinIsFlow(iPinType):
                iDataType = -1
            else:
                iDataType = interface.GetPinAttr(self.m_PinID, bddefine.PinAttrName.DATA_TYPE)
        icon = QIcon()
        pix = ":/icon/btn_%s.png" % iDataType
        icon.addPixmap(QPixmap(pix), QIcon.Normal, QIcon.Off)
        self.m_Btn.setIcon(icon)

    def SetText(self, sText=None):
        if sText is None:
            sText = interface.GetPinAttr(self.m_PinID, bddefine.PinAttrName.DISPLAYNAME)
        self.m_Label.setText(sText)

    def SetWidget(self):
        iPinType = interface.GetPinAttr(self.m_PinID, bddefine.PinAttrName.PIN_TYPE)
        if iPinType != bddefine.PIN_INPUT_DATA_TYPE:
            return
        if self.m_Widget:
            self.m_Widget.setParent(None)
            index = self.m_HLayout.itemAt(self.m_Widget)
            item = self.m_HLayout.itemAt(index)
            self.m_HLayout.removeWidget(self.m_Widget)
            self.m_HLayout.removeItem(item)
            self.m_Widget = None


class CTypeButton(QPushButton):
    def __init__(self, pinID, parent=None):
        super(CTypeButton, self).__init__(parent)
        self.m_PinID = pinID

    def _InitUI(self):
        self.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFlat(False)
        self.setIconSize(QSize(20, 20))

    # def mousePressEvent(self, event):
    #     super(CTypeButton, self).mousePressEvent(event)
    #     if event.button() == Qt.LeftButton:
    #         self.scene().BeginConnect(self.m_PinID)
    #     event.accept()

    # def mouseMoveEvent(self, event):
    #     super(CTypeButton, self).mouseMoveEvent(event)
    #     event.accept()
    #     if event.button() == Qt.LeftButton:
    #         self.update()

    # def mouseReleaseEvent(self, event):
    #     event.accept()
    #     super(CTypeButton, self).mouseReleaseEvent(event)
    #     if event.button() == Qt.LeftButton:
    #         self.scene().EndConnect(event)
