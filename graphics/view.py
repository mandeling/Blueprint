# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-08 16:44:23
@Desc: 蓝图
"""
import sys
import misc

from . import scene
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QMenu, QAction
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt


class CBlueprintView(QGraphicsView):
    def __init__(self, parent=None):
        super(CBlueprintView, self).__init__(parent)
        self.m_Scale = 1
        self.m_StartPos = None
        self.m_Scene = scene.CBlueprintScene(self)
        self.Init()

    def Init(self):
        self.setScene(self.m_Scene)
        self.setGeometry(300, 200, 600, 400)
        self.setBackgroundBrush(QBrush(QColor(103, 103, 103), Qt.SolidPattern))
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setResizeAnchor(QGraphicsView.NoAnchor)

    def mousePressEvent(self, event):
        super(CBlueprintView, self).mousePressEvent(event)
        print("mousePressEvent")

    def mouseMoveEvent(self, event):
        super(CBlueprintView, self).mouseMoveEvent(event)
        # print("mouseMoveEvent")

    def contextMenuEvent(self, event):
        """右键上下文事件"""
        super(CBlueprintView, self).contextMenuEvent(event)
        print("contextMenuEvent")
        gPos1 = event.pos()
        gPos2 = self.mapToGlobal(gPos1)
        pos1 = self.mapFromGlobal(gPos2)
        pos = pos1.x(), pos1.y()
        menu = QMenu(self)
        print(gPos1, gPos2, pos1, pos)
        lstMenu = ["添加", "删除", "移动"]
        for iIndex, sName in enumerate(lstMenu):
            func = misc.Functor(self.OnCreateAction, iIndex, pos, sName)
            action = QAction(sName, self)
            action.triggered.connect(func)
            menu.addAction(action)
        menu.exec_(gPos2)

    def OnCreateAction(self, *args):
        print("OnCreateAction:", args)



