# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-08 16:44:23
@Desc: 蓝图view
"""

from . import scene
from editdata import interface

from PyQt5.QtWidgets import QGraphicsView, QMenu, QRubberBand
from PyQt5.QtGui import QBrush, QColor, QPainterPath
from PyQt5.QtCore import Qt, QRect

from pubcode import functor
from viewmgr.uimgr import GetUIMgr
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
        GetUIMgr().AddGraphicView(graphicID, self)
        self._LoadData()

    def __del__(self):
        GetUIMgr().DelGraphicView(self.m_GraphicID)

    def _InitUI(self):
        self.setWindowTitle("蓝图")
        self.setScene(self.m_Scene)
        self.setBackgroundBrush(QBrush(QColor(103, 103, 103), Qt.SolidPattern))
        self.setDragMode(QGraphicsView.NoDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        # 隐藏滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def _LoadData(self):
        lstNode = interface.GetGraphicAttr(self.m_GraphicID, eddefine.GraphicAttrName.NODE_LIST)
        for nodeID in lstNode:
            tPos = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.POSITION)
            self.m_Scene.AddNodeUI(nodeID, tPos)
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
        if event.modifiers() == Qt.ControlModifier:
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
            return
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
        if not self.CanDrag(event):
            event.ignore()
            return
        event.accept()
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        """拖拽移动中"""
        if not self.CanDrag(event):
            event.ignore()
            return
        event.accept()
        event.acceptProposedAction()

    def dropEvent(self, event):
        """放开了鼠标完成drop操作"""
        super(CBlueprintView, self).dropEvent(event)
        if not self.CanDrag(event):
            event.ignore()
            return
        event.acceptProposedAction()
        lPos = event.pos()
        sPos = self.mapToScene(lPos)
        tPos = sPos.x(), sPos.y()
        # TODO mimeData

    def CanDrag(self, event):
        # TODO
        return True

    def S_OnCreateNodeUI(self, sNodeName, tPos):
        nodeID = interface.AddNode(self.m_GraphicID, sNodeName, tPos)
        self.m_Scene.AddNodeUI(nodeID, tPos)
