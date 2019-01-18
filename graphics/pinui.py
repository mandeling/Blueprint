# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-14 14:58:39
@Desc: 节点槽UI
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QSizePolicy, QMenu
from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QCursor

import bpdata.define as bddefine
from . import subpinui
from editdata import interface
from viewmgr.uimgr import GetUIMgr
from pubcode import functor
from signalmgr import GetSignal


class CPinUI(QWidget):
    def __init__(self, pinID, parent=None):
        super(CPinUI, self).__init__(parent)
        self.m_PinID = pinID
        self.m_NodeID = interface.GetNodeIDByPinID(pinID)
        self.m_GraphicID = interface.GetGraphicIDByNodeID(self.m_NodeID)
        self.m_Btn = None
        self.m_Label = None
        self.m_HLayout = None
        self.m_DefaultWidget = None  # 默认值控件
        self._InitUI()
        self.SetIcon()
        self.SetText()
        self.ShowDefaultWidget()
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

    def contextMenuEvent(self, event):
        super(CPinUI, self).contextMenuEvent(event)
        lstLineID = interface.GetAllLineByPin(self.m_PinID)
        menu = QMenu()
        for lineID in lstLineID:
            oPinID = interface.GetLineOtherPin(lineID, self.m_PinID)
            sPinDisplayName = interface.GetPinAttr(oPinID, bddefine.PinAttrName.DISPLAYNAME)
            nodeID = interface.GetNodeIDByPinID(oPinID)
            sNodeDisplayName = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.DISPLAYNAME)
            sMsg = "删除与\"%s\"-\"%s\"的连线" % (sNodeDisplayName, sPinDisplayName)
            func = functor.Functor(interface.DelLine, lineID)
            menu.addAction(sMsg, func)
        menu.exec_(QCursor.pos())
        event.accept()

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

    def ShowDefaultWidget(self):
        iPinType = interface.GetPinAttr(self.m_PinID, bddefine.PinAttrName.PIN_TYPE)
        if iPinType != bddefine.PIN_INPUT_DATA_TYPE:
            return
        lstLine = interface.GetAllLineByPin(self.m_PinID)
        if lstLine:
            return
        oWidget = None
        iDataTye = interface.GetPinAttr(self.m_PinID, bddefine.PinAttrName.DATA_TYPE)
        if iDataTye in (bddefine.Type.INT, bddefine.Type.FLOAT, bddefine.Type.STR):
            oWidget = subpinui.CValidatorLineEdit(self.m_PinID, iDataTye)
        elif iDataTye == bddefine.Type.BOOL:
            oWidget = subpinui.CCheckBox(self.m_PinID)
        if oWidget:
            self.m_HLayout.addWidget(oWidget)
            self.m_DefaultWidget = oWidget
            self.adjustSize()

    def HideDefaultWidget(self):
        if not self.m_DefaultWidget:
            return
        self.m_DefaultWidget.setParent(None)
        index = self.m_HLayout.indexOf(self.m_DefaultWidget)
        item = self.m_HLayout.itemAt(index)
        self.m_HLayout.removeWidget(self.m_DefaultWidget)
        self.m_HLayout.removeItem(item)
        self.m_DefaultWidget = None
        self.adjustSize()

    def enterEvent(self, event):
        super(CPinUI, self).enterEvent(event)
        GetSignal().UI_LINE_CONNECT.emit(self.m_GraphicID, self.m_PinID)
        event.accept()


class CTypeButton(QPushButton):
    def __init__(self, pinID, parent=None):
        super(CTypeButton, self).__init__(parent)
        self.m_PinID = pinID
        self.m_NodeID = interface.GetNodeIDByPinID(pinID)
        self.m_GraphicID = interface.GetGraphicIDByNodeID(self.m_NodeID)
        self.m_IsInputPin = interface.IsInputPin(pinID)
        self.m_Center = None
        self._InitUI()
        GetUIMgr().AddPinBtnUI(pinID, self)

    def __del__(self):
        GetUIMgr().DelPinBtnUI(self.m_PinID)

    def _InitUI(self):
        self.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFlat(False)
        size = QSize(20, 20)
        self.setIconSize(size)
        self.setMinimumSize(size)
        self.setMaximumSize(size)

    def GetCenter(self):
        if not self.m_Center:
            x, y = self.size().width(), self.size().height()
            if self.m_IsInputPin:
                self.m_Center = 0, y / 2
            else:
                self.m_Center = x, y / 2
        return self.m_Center

    def GetScenePos(self):
        ePos = QPoint(*self.GetCenter())
        nodeUI = GetUIMgr().GetNodeUI(self.m_NodeID)
        nPos = self.mapTo(nodeUI.m_NodeWidget, ePos)
        sPos = nodeUI.mapToScene(nPos)
        return sPos

    def mousePressEvent(self, event):
        super(CTypeButton, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            GetSignal().UI_LINE_PRESS.emit(self.m_GraphicID, self.m_PinID)
        event.accept()

    def mouseMoveEvent(self, event):
        super(CTypeButton, self).mouseMoveEvent(event)
        if event.button() == Qt.LeftButton:
            GetSignal().UI_LINE_MOVE.emit(self.m_GraphicID)
        event.accept()

    def mouseReleaseEvent(self, event):
        super(CTypeButton, self).mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            GetSignal().UI_LINE_RELEASE.emit(self.m_GraphicID)
        event.accept()
