# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-09 09:55:45
@Desc: 
"""

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QMenu, QAction
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt

from . import item


class CBlueprintScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(CBlueprintScene, self).__init__(parent)
        self.m_ItemList = []
        self.Init()

    def Init(self):
        self.setSceneRect(0, 0, 400, 300)

    def mousePressEvent(self, event):
        super(CBlueprintScene, self).mousePressEvent(event)
        print("scene.mousePressEvent")
        if event.isAccepted():
            return
        if event.button() == Qt.LeftButton:
            point = event.scenePos()
            sceneRect = self.sceneRect()
            oItem = item.CBlueprintItem(sceneRect)
            oItem.setPos(point.x(), point.y())
            self.addItem(oItem)
            self.m_ItemList.append(oItem)
