from PyQt5.QtWidgets import QWidget, QGraphicsPolygonItem, QGraphicsPathItem, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QColor, QBrush, QPen, QPainterPath, QPainter, QPolygonF

import weakref

from .slotmgr import GetSlotMgr


class CWidget(QWidget):
    def __init__(self, parent=None):
        super(CWidget, self).__init__(parent)
        self.m_Stype = {}
        self.setCursor(Qt.SizeAllCursor)

    def mousePressEvent(self, event):
        event.accept()

    def GetStyle(self):
        style = self.styleSheet()
        self.m_Stype["Widget"] = ""
        self.m_Stype["Press"] = ""
        sWidgetStyle = "QWidget#outline{background:transparent;}"
        sWidgetPressStr = "QWidget#outline{"
        sWidgetPressStyle = ""
        iIndex = style.find(sWidgetPressStr)
        if iIndex != -1:
            tmpStyle = style[iIndex:]
            iEnd = tmpStyle.find("}") + 1
            sWidgetPressStyle = tmpStyle[:iEnd]
            style = style.replace(sWidgetPressStyle, "")
        self.m_Stype["Widget"] = style + sWidgetStyle
        self.m_Stype["Press"] = style + sWidgetPressStyle

    def SetStyle(self, state):
        self.setStyleSheet(self.m_Stype.get(state, ""))


class CSlotUI(QGraphicsPolygonItem):
    def __init__(self, uid, oSlot, parent=None):
        super(CSlotUI, self).__init__(parent)
        self.m_Uid = uid
        self.m_Slot = weakref.ref(oSlot)
        self.m_LintItem = None
        self.m_IsLineMoving = False  # 是否在划线
        self.m_DownPosition = None   # 划线的起始坐标（相对于场景）
        self.m_CurPos = None         # 划线当前的坐标（相对于场景）
        self.InitUI()

    def InitUI(self):
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setZValue(4)
        self.setAcceptHoverEvents(True)

        size = self.m_Slot().GetSize()
        self.m_PF = QRectF(0, 0, size[0], size[1])
        self.setPolygon(QPolygonF(self.m_PF))
        self.setCursor(Qt.CrossCursor)

    def mousePressEvent(self, event):
        print("slotui-mousePressEvent", self.scene())
        super(CSlotUI, self).mousePressEvent(event)
        event.accept()
        if event.button() == Qt.LeftButton:
            self.scene().BeginConnect(self)
            # self.m_DownPosition = event.buttonDownScenePos(Qt.LeftButton)

    def mouseMoveEvent(self, event):
        print("slotui-mouseMoveEvent")
        super(CSlotUI, self).mouseMoveEvent(event)
        event.accept()
        if event.button() == Qt.LeftButton and self.m_DownPosition:
            self.m_IsLineMoving = True
            self.m_CurPos = event.scenePos()
            self.update()

            lastuid = GetSlotMgr().GetLastSelect()
            if not lastuid:
                GetSlotMgr().SetLastSelect(self.m_Uid)

    def mouseReleaseEvent(self, event):
        print("slotui-mouseReleaseEvent")
        event.accept()
        super(CSlotUI, self).mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.scene().EndConnect(self)
            self.m_IsLineMoving = False
            self.m_DownPosition = None
            self.m_CurPos = None

    def paint(self, painter, qStyleOptionGraphicsItem, widget):
        color = QColor(Qt.yellow)
        brush = QBrush(color)
        pen = QPen(color)
        pen.setWidth(2)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawRect(self.m_PF)
        # if not self.m_LintItem:
        #     self.m_LintItem = QGraphicsPathItem(self)
        # path = QPainterPath()
        # if self.m_IsLineMoving:
        #     self.prepareGeometryChange()
        #     painter.setRenderHint(QPainter.Antialiasing, True)
        #     path.moveTo(*self.m_Slot().GetCenter())
        #     point = self.m_CurPos - QPointF(*self.m_Slot().GetPos()) + QPointF(*self.m_Slot().GetCenter())
        #     print("---", self.m_Slot().GetCenter(), point)
        #     path.lineTo(point)
        # self.m_LintItem.setPath(path)
        # painter.drawPath(path)

    def hoverEnterEvent(self, event):
        # print("slotui-hoverEnterEvent")
        super(CSlotUI, self).hoverEnterEvent(event)

    def hoverMoveEvent(self, event):
        # print("slotui-hoverMoveEvent")
        super(CSlotUI, self).hoverMoveEvent(event)

    def hoverLeaveEvent(self, event):
        # print("slotui-hoverLeaveEvent")
        super(CSlotUI, self).hoverLeaveEvent(event)
