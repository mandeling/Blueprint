# -*- coding:utf-8 -*-
"""
@Author: xiaohao
@Date: 2018-11-21 14:48:22
@Desc: 节点ui
"""

import weakref
import miscqt

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsTextItem, QGraphicsItem, QPushButton, QWidget
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPoint
from PyQt5.QtGui import QFont

from . import slotui, config, define
from .slotmgr import GetSlotMgr


class CBlueChartUI(QGraphicsProxyWidget):
    def __init__(self, oBlueChart, sName, oScene, parent=None):
        super(CBlueChartUI, self).__init__(parent)
        self.m_Uid = oBlueChart.GetID()
        self.m_BlueChart = weakref.ref(oBlueChart)
        self.m_Name = sName
        self.m_Scene = weakref.ref(oScene)
        self.m_StartPos = None
        self.m_ChartIsMoving = False
        self.m_BlueChartWidget = CBlueChartWidget(sName, config.CHART_DATA[sName])
        self.m_ChangeCharName = None
        self.InitUI()
        self.InitSlot()
        self.InitSingle()

    def InitUI(self):
        sName = self.m_BlueChart().GetName()
        self.m_BlueChartWidget.lb_Title.setText(sName)

        self.m_ChangeCharName = CGraphicsTextItem(self.GetTitle(), self)
        self.m_ChangeCharName.setParentItem(self)
        self.m_ChangeCharName.setTextWidth(self.m_BlueChartWidget.top.width())
        self.m_ChangeCharName.hide()

        self.setWidget(self.m_BlueChartWidget)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setZValue(4)

    def InitSlot(self):
        """四个槽的初始化,先手动设置"""
        for uid, oBtn in self.m_BlueChartWidget.m_ButtonInfo.items():
            qpos = oBtn.mapToParent(QPoint(0, 0))
            pos = (qpos.x(), qpos.y())
            size = (oBtn.width(), oBtn.height())
            oSlot = GetSlotMgr().NewSlot(self.m_Uid, pos, size, oBtn)
            oSlotUI = slotui.CSlotUI(uid, oSlot)
            oSlotUI.setParentItem(self)
            x, y = self.pos().x(), self.pos().y()
            x += oBtn.x()
            y += oBtn.y()
            mfsPos = oSlotUI.mapFromScene(x, y)
            mtpPos = oSlotUI.mapToParent(mfsPos)
            oSlotUI.setPos(mtpPos.x(), mtpPos.y())
            GetSlotMgr().AddSlotUI(uid, oSlotUI)

    def InitSingle(self):
        self.m_ChangeCharName.SING_CHANGE_TITLE.connect(self.S_ChangeName)

    def IsDrawLine(self):
        return self.m_Scene().m_IsDrawLine

    def mousePressEvent(self, event):
        super(CBlueChartUI, self).mousePressEvent(event)
        event.accept()
        if self.IsDrawLine():
            return
        if event.button() == Qt.LeftButton:
            self.m_StartPos = event.pos()
            self.m_ChartIsMoving = False

    def mouseMoveEvent(self, event):
        super(CBlueChartUI, self).mouseMoveEvent(event)
        if self.IsDrawLine():
            return
        self.SetMouseMovePos(self.m_StartPos, event.pos())

    def mouseReleaseEvent(self, event):
        super(CBlueChartUI, self).mouseReleaseEvent(event)
        if self.isSelected() and event.button() == Qt.LeftButton:
            pos = event.pos()
            rect = QRectF(self.m_BlueChartWidget.top.rect())
            rect.setWidth(rect.width() / 2)
            if rect.contains(pos):
                self.m_ChangeCharName.show()
                self.m_ChangeCharName.setPlainText(self.GetTitle())
                self.m_BlueChartWidget.lb_Title.hide()
        self.setSelected(True)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for _, oSlotUI in GetSlotMgr().GetAllSlotUI().items():
                oSlotUI.UpdateLinePosition()
        return super(CBlueChartUI, self).itemChange(change, value)

    def GetTitle(self):
        return self.m_BlueChartWidget.lb_Title.text()

    def SetMouseMovePos(self, sPos, ePos):
        if not (sPos and ePos):
            return
        pos = self.pos()
        x = pos.x() + ePos.x() - sPos.x()
        y = pos.y() + ePos.y() - sPos.y()
        self.setPos(x, y)

    def S_ChangeName(self, sTitle):
        sOldTitle = self.GetTitle()
        if sOldTitle != sTitle:
            self.m_BlueChartWidget.lb_Title.setText(sTitle)
            self.m_BlueChart().SetName(sTitle)
        self.m_BlueChartWidget.lb_Title.show()


class CGraphicsTextItem(QGraphicsTextItem):

    SING_CHANGE_TITLE = pyqtSignal(str)

    def __init__(self, sName, parent=None):
        super(CGraphicsTextItem, self).__init__(sName, parent)
        self.Init()

    def Init(self):
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setCursor(Qt.IBeamCursor)

        font = QFont()
        font.setPixelSize(18)
        self.setFont(font)
        self.setZValue(8)
        self.setPos(10, 10)

    def focusOutEvent(self, event):
        super(CGraphicsTextItem, self).focusOutEvent(event)
        sTitle = self.toPlainText()
        if sTitle:
            self.SING_CHANGE_TITLE.emit(sTitle)
        self.setPlainText("")
        self.hide()


QSS_STYLE = """
QWidget#CBlueChartWidget{
    background:transparent;
}
QWidget#BCWidget{
    background:rgba(0, 0, 0, 200);
    border-style:solid;
    border-width:0px;
    border-radius:10px;
}
QWidget#top{
    border-style:solid;
    border-width:0px;
    background:qlineargradient(spread:pad, x1:0.00564972, y1:0.358, x2:1, y2:0.637, stop:0 rgba(0, 104, 183, 200), stop:1 rgba(0, 160, 233, 50));
    border-top-left-radius:10px;
    border-top-right-radius:10px;
    border-bottom-left-radius:0px;
    border-bottom-right-radius:0px;
}
QLabel{
    color:white;
}
QPushButton{
    background-color:transparent;
    color:white;
    border:none;
}
QPushButton:hover{
    background:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(255, 0, 0, 0), stop:0.175141 rgba(255, 255, 255, 100), stop:0.824859 rgba(255, 255, 255, 100), stop:1 rgba(0, 0, 255, 0));
    border-image:transparent;
    color:white;
}
QWidget#outline{
    background:transparent;
    border:4px solid rgb(244, 100, 0);
    border-radius:14px;
}
"""


class CBlueChartWidget(QWidget):
    def __init__(self, sName, dInfo, parent=None):
        super(CBlueChartWidget, self).__init__(parent)
        self.m_Name = sName
        self.m_InputInfo = dInfo.get("input", [])
        self.m_OutputInfo = dInfo.get("output", [])
        self.m_ButtonInfo = {}
        self.InitUI()

    def AddButton(self, oBtn):
        if not oBtn:
            return
        self.m_ButtonInfo[oBtn.GetUid()] = oBtn

    def InitUI(self):
        self.setObjectName("CBlueChartWidget")
        self.setStyleSheet(QSS_STYLE)
        self.setCursor(Qt.SizeAllCursor)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.BCWidget = QtWidgets.QWidget(self)
        self.BCWidget.setObjectName("BCWidget")
        self.verticalLayout_BCWidget = QtWidgets.QVBoxLayout(self.BCWidget)
        self.verticalLayout_BCWidget.setObjectName("verticalLayout_BCWidget")

        # top
        self.top = QtWidgets.QWidget(self.BCWidget)
        self.top.setObjectName("top")
        self.horizontalLayout_top = QtWidgets.QHBoxLayout(self.top)
        self.horizontalLayout_top.setContentsMargins(6, 2, 4, 2)
        self.horizontalLayout_top.setObjectName("horizontalLayout_top")
        self.lb_Title = QtWidgets.QLabel(self.top)
        self.lb_Title.setObjectName("lb_Title")
        self.lb_Title.setText(self.m_Name)
        self.horizontalLayout_top.addWidget(self.lb_Title)
        spacerItem = QtWidgets.QSpacerItem(67, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_top.addItem(spacerItem)
        self.verticalLayout_BCWidget.addWidget(self.top)

        # for attr
        maxLen = max(len(self.m_InputInfo), len(self.m_OutputInfo))
        for i in range(maxLen):
            qHL = QtWidgets.QHBoxLayout()
            oInBtn = oOutBtn = None
            if i < len(self.m_InputInfo) and self.m_InputInfo[i]:
                oInBtn = CChartButtonUI(define.INPUT_BTN_TYPE, self.m_InputInfo[i], self.BCWidget)
            if i < len(self.m_OutputInfo) and self.m_OutputInfo[i]:
                oOutBtn = CChartButtonUI(define.OUTPUT_BTN_TYPE, self.m_OutputInfo[i], self.BCWidget)
            spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            if oInBtn:
                qHL.addWidget(oInBtn)
                self.AddButton(oInBtn)
            qHL.addItem(spacerItem)
            if oOutBtn:
                qHL.addWidget(oOutBtn)
                self.AddButton(oOutBtn)
            self.verticalLayout_BCWidget.addLayout(qHL)

        self.verticalLayout.addWidget(self.BCWidget)


class CChartButtonUI(QPushButton):
    def __init__(self, iType, dInfo, parent=None):
        super(CChartButtonUI, self).__init__(parent)
        self.m_SlotType = iType
        self.m_VarType = dInfo["type"]
        self.m_Name = dInfo["name"]
        self.m_UID = miscqt.NewUuid()
        self.InitUI()

    def InitUI(self):
        self.setCursor(Qt.PointingHandCursor)
        if self.m_SlotType == define.OUTPUT_BTN_TYPE:
            self.setLayoutDirection(QtCore.Qt.RightToLeft)
        icon = QtGui.QIcon()
        pix = ":/icon/btn_%s.png" % self.m_VarType
        icon.addPixmap(QtGui.QPixmap(pix), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(icon)
        self.setIconSize(QtCore.QSize(20, 20))
        self.setText(self.m_Name)

    def GetUid(self):
        return self.m_UID

    def GetSlotType(self):
        return self.m_SlotType

    def GetVarType(self):
        return self.m_VarType

    def mousePressEvent(self, event):
        super(CChartButtonUI, self).mousePressEvent(event)
        event.accept()
        print("CChartButtonUI mousePressEvent", self.m_UID)

    def mouseMoveEvent(self, event):
        super(CChartButtonUI, self).mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        super(CChartButtonUI, self).mouseReleaseEvent(event)
        event.accept()
