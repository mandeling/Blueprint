# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-08 16:44:23
@Desc: 蓝图view
"""
import misc

from . import scene, uimgr
from editdata import interface

from PyQt5.QtWidgets import QGraphicsView, QMenu
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt


class CBlueprintView(QGraphicsView):
    def __init__(self, bpID, parent=None):
        super(CBlueprintView, self).__init__(parent)
        self.m_BPID = bpID
        self.m_Scale = 1
        self.m_StartPos = None
        self.m_Scene = scene.CBlueprintScene(bpID, self)
        self.Init()
        uimgr.GetUIMgr().AddBPView(bpID, self)

    def Init(self):
        self.setWindowTitle("蓝图")
        self.setScene(self.m_Scene)
        # self.setGeometry(300, 150, 1200, 800)
        self.setBackgroundBrush(QBrush(QColor(103, 103, 103), Qt.SolidPattern))
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        # 隐藏滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def GetBPID(self):
        return self.m_BPID

    def mousePressEvent(self, event):
        super(CBlueprintView, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)
        else:
            self.setDragMode(QGraphicsView.NoDrag)

        if event.button() == Qt.MidButton:
            self.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.m_StartPos = event.pos()

    def mouseMoveEvent(self, event):
        super(CBlueprintView, self).mouseMoveEvent(event)
        if not self.m_StartPos:
            return
        pos = event.pos()
        offsetX, offsetY = pos.x() - self.m_StartPos.x(), pos.y()-self.m_StartPos.y()
        offsetX /= self.m_Scale
        offsetY /= self.m_Scale
        self.translate(offsetX, offsetY)
        self.m_StartPos = pos

    def mouseReleaseEvent(self, event):
        super(CBlueprintView, self).mouseReleaseEvent(event)
        if event.button() == Qt.MidButton:
            self.m_StartPos = None
        self.setDragMode(QGraphicsView.RubberBandDrag)

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
        if event.isAccepted():
            return
        lPos = event.pos()
        gPos = self.mapToGlobal(lPos)
        sPos = self.mapToScene(lPos)
        tPos = sPos.x(), sPos.y()
        menu = QMenu(self)
        for sNodeName in interface.GetAllDefineNodeName():
            func = misc.Functor(self.S_OnCreateNodeUI, sNodeName, tPos)
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

    def CreateNodeUI(self, nodeID, tPos):
        self.m_Scene.AddNodeUI(nodeID, tPos)
        interface.SetNodeAttr(self.m_BPID, nodeID, 1, 2)

    def S_OnCreateNodeUI(self, sNodeName, tPos):
        nodeID = interface.AddNode(self.m_BPID, sNodeName)
        self.CreateNodeUI(nodeID, tPos)
