# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-09 10:33:39
@Desc: 
"""
import math

from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QApplication, QMenu, QAction
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QPoint


class CBlueprintItem(QGraphicsItem):
    def __init__(self, rect, parent=None):
        super(CBlueprintItem, self).__init__(parent)
        self.m_Rect = rect
        self.m_Resizing = True
        self.m_CenterPoint = False
        self.Init()


    def Init(self):
        # self.setRect(0, 0, 200, 100)
        # color = QColor(247, 160, 57)
        # pen = QPen(color)
        # pen.setWidth(20)  # 画笔

        # self.setPen(pen)
        # self.setBrush(QColor(12, 56, 123))
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return self.m_Rect

    def paint(self, painter, option, widget):
        super(CBlueprintItem, self).paint(painter, option, widget)
        bgRect = self.boundingRect()
        painter.drawRects(bgRect)
        painter.fillRect(bgRect, QColor(247, 160, 57))

    def mousePressEvent(self, event):
        print("item.mousePressEvent")
        if event.button() == Qt.LeftButton:
            if event.modifiers() == Qt.ShiftModifier:
                print("Custom item left clicked with shift key.")
                self.setSelected(True)
            elif event.modifiers() == Qt.AltModifier:
                print("Custom item left clicked with alt key.")
                r = self.boundingRect().width() / 2.0
                topLeft = self.boundingRect().topLeft()
                self.m_CenterPoint = QPoint(topLeft.x() + self.pos().x() + r, topLeft.y() + self.pos().y() + r)
                pos = event.scenePos()
                dis = self._GetCenterPointDis(pos)
                if dis/r > 0.8:
                    self.m_Resizing = True
                else:
                    self.m_Resizing = False
            else:
                print("Custom item left clicked.")
                super(CBlueprintItem, self).mousePressEvent(event)
                event.accept()
        elif event.button() == Qt.RightButton:
            event.ignore()

    def _GetCenterPointDis(self, pos):
        dis = math.sqrt(math.pow(self.m_CenterPoint.x() - pos.x(), 2) + math.pow(self.m_CenterPoint.y()-pos.y(), 2))
        return dis

    def mouseMoveEvent(self, event):
        print("item.mouseMoveEvent")
        if event.modifiers() == Qt.AltModifier and self.m_Resizing:
            pos = event.scenePos()
            dist = self._GetCenterPointDis(pos)
            self.setRect(self.m_CenterPoint.x() - self.pos().x()-dist, self.m_CenterPoint.y()-self.pos().y()-dist, dist*2, dist*2)
        elif event.modifiers() != Qt.AltModifier:
            super(CBlueprintItem, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        print("item.mouseReleaseEvent")
        if event.modifiers() == Qt.AltModifier and self.m_Resizing:
            self.m_Resizing = False
        else:
            super(CBlueprintItem, self).mouseReleaseEvent(event)
