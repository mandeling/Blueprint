# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-08 16:44:23
@Desc: 蓝图view
"""

from . import scene
from editdata import interface

from PyQt5.QtWidgets import QGraphicsView, QMenu, QRubberBand
from PyQt5.QtGui import QBrush, QColor, QPainterPath, QCursor
from PyQt5.QtCore import Qt, QRect, QPointF

from pubcode import functor
from viewmgr.uimgr import GetUIMgr
from viewmgr.statusmgr import GetStatusMgr
from signalmgr import GetSignal
import editdata.define as eddefine
import bpdata.define as bddefine


class CBlueprintView(QGraphicsView):
    def __init__(self, graphicID, parent=None):
        super(CBlueprintView, self).__init__(parent)
        self.m_GraphicID = graphicID
        self.m_Scale = 1
        self.m_StartPos = None
        self.m_IsHasMove = False    # view视图是否有移动
        self.m_SelectPos = None     # 框选初始坐标
        self.m_RubberBand = None    # 框选框对象
        self.m_Scene = scene.CBlueprintScene(graphicID, self)
        self._InitUI()
        self._InitSignal()
        self._LoadData()

    def _InitUI(self):
        self.setWindowTitle("蓝图")
        self.setScene(self.m_Scene)
        # self.setBackgroundBrush(QBrush(QColor(103, 103, 103), Qt.SolidPattern))
        self.setDragMode(QGraphicsView.NoDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        # 隐藏滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def _InitSignal(self):
        GetSignal().UI_FOCUS_NODE.connect(self.S_FocusNode)

    def _LoadData(self):
        lstNode = interface.GetGraphicAttr(self.m_GraphicID, eddefine.GraphicAttrName.NODE_LIST)
        for nodeID in lstNode:
            self.m_Scene._NewNodeUI(nodeID)
        lstLine = interface.GetGraphicAttr(self.m_GraphicID, eddefine.GraphicAttrName.LINE_LIST)
        for lineID in lstLine:
            iPinID, oPinID = interface.GetLinePinInfo(lineID)
            self.m_Scene.AddLineUI(lineID, iPinID, oPinID)

    def GetGraphicID(self):
        return self.m_GraphicID

    def mousePressEvent(self, event):
        super(CBlueprintView, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            if self.itemAt(event.pos()) is None:
                self.m_SelectPos = event.pos()
                self.setDragMode(QGraphicsView.NoDrag)
                self.setTransformationAnchor(QGraphicsView.NoAnchor)
                self.m_RubberBand = QRubberBand(QRubberBand.Rectangle, self.viewport())
                self.m_RubberBand.show()

        if event.button() == Qt.MidButton:
            self.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.m_StartPos = event.pos()

    def mouseMoveEvent(self, event):
        super(CBlueprintView, self).mouseMoveEvent(event)
        pos = event.pos()
        if self.m_StartPos:
            offsetX, offsetY = pos.x() - self.m_StartPos.x(), pos.y()-self.m_StartPos.y()
            offsetX /= self.m_Scale
            offsetY /= self.m_Scale
            self.translate(offsetX, offsetY)
            self.m_StartPos = pos
            self.m_IsHasMove = True

        if self.m_SelectPos:
            rect = QRect(
                min(self.m_SelectPos.x(), pos.x()),
                min(self.m_SelectPos.y(), pos.y()),
                abs(self.m_SelectPos.x() - pos.x()),
                abs(self.m_SelectPos.y() - pos.y())
            )
            path = QPainterPath()
            path.addPolygon(self.mapToScene(rect))
            path.closeSubpath()
            self.m_Scene.RubberBandSelecNodeUI(path, self.rubberBandSelectionMode(), self.viewportTransform())
            self.m_RubberBand.setGeometry(rect)

    def mouseReleaseEvent(self, event):
        super(CBlueprintView, self).mouseReleaseEvent(event)
        if event.button() == Qt.MidButton:
            self.m_StartPos = None
            self.setDragMode(QGraphicsView.NoDrag)
        if event.button() == Qt.LeftButton:
            self.m_SelectPos = None
            if self.m_RubberBand:
                self.m_RubberBand.setParent(None)
                self.m_RubberBand = None

    def wheelEvent(self, event):
        """ctrl+滑轮滚动缩放"""
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        fAngleDelta = event.angleDelta().y()
        factor = 1.41 ** (fAngleDelta / 240.0)
        minScale, maxScale = 0.1, 2.0   # 控制缩放的值
        fNewScale = self.m_Scale * factor
        if fNewScale > maxScale:
            fNewScale = maxScale
        elif fNewScale < minScale:
            fNewScale = minScale
        fScale = fNewScale / self.m_Scale
        self.scale(fScale, fScale)
        self.m_Scale = fNewScale
        # 没有缩放信号传递给下层
        super(CBlueprintView, self).wheelEvent(event)
        event.ignore()

    def contextMenuEvent(self, event):
        """右键上下文事件"""
        super(CBlueprintView, self).contextMenuEvent(event)
        if self.m_IsHasMove:
            self.m_IsHasMove = False
            return
        if event.isAccepted():
            return
        lPos = event.pos()
        gPos = self.mapToGlobal(lPos)
        sPos = self.mapToScene(lPos)
        tPos = sPos.x(), sPos.y()
        menu = QMenu(self)
        for sNodeName in interface.GetAllDefineNodeName():
            func = functor.Functor(self.S_OnCreateNodeUI, sNodeName, tPos)
            menu.addAction(sNodeName, func)
        menu.exec_(gPos)

    def dragEnterEvent(self, event):
        """拖动操作进入本窗口"""
        super(CBlueprintView, self).dragEnterEvent(event)
        event.accept()
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        """拖拽移动中"""
        event.accept()
        event.acceptProposedAction()

    def dropEvent(self, event):
        """放开了鼠标完成drop操作"""
        super(CBlueprintView, self).dropEvent(event)
        event.acceptProposedAction()
        oMimeData = event.mimeData()
        from bpwidget.bpattrui import basetree
        from bpwidget import define as bwdefine
        if not isinstance(oMimeData, basetree.CBPAttrMimeData):
            return
        sType, varID = oMimeData.GetItemInfo()
        if sType != bwdefine.BP_ATTR_VARIABLE:
            return
        lPos = event.pos()
        sPos = self.mapToScene(lPos)
        tPos = sPos.x(), sPos.y()
        menu = QMenu(self)
        for sNodeName in (bddefine.NodeName.GET_VARIABLE, bddefine.NodeName.SET_VARIABLE):
            func = functor.Functor(self.S_OnCreateNodeUI, sNodeName, tPos, varID)
            menu.addAction(sNodeName, func)
        menu.exec_(QCursor.pos())

    def S_OnCreateNodeUI(self, sNodeName, tPos=(0, 0), varID=None):
        interface.AddNode(self.m_GraphicID, sNodeName, tPos, varID)

    def S_FocusNode(self, graphicID, nodeID):
        if self.m_GraphicID != graphicID:
            return

        bpID = interface.GetBPIDByGraphicID(graphicID)
        GetSignal().UI_FOCUS_GRAPHIC.emit(bpID, graphicID)

        pos = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.POSITION)
        x, y = pos[0], pos[1]
        oNodeUI = GetUIMgr().GetNodeUI(nodeID)
        if oNodeUI:
            x += oNodeUI.size().width() / 2
            y += oNodeUI.size().height() / 2
        point = QPointF(x, y)
        self.centerOn(point)
        GetStatusMgr().SelectOneNode(graphicID, nodeID)
