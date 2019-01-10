# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-28 18:58:37
@Desc: 蓝图菜单控件
"""


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize


class CMenuUI(QWidget):
    def __init__(self, bpID, parent=None):
        super(CMenuUI, self).__init__(parent)
        self.m_BPID = bpID
        self._InitUI()

    def _InitUI(self):
        horizontalLayout = QHBoxLayout(self)
        horizontalLayout.addWidget(self._GetButton("保存", "save", self.S_Save))
        horizontalLayout.addWidget(self._GetButton("开始", "start", self.S_Start))
        horizontalLayout.addWidget(self._GetButton("停止", "stop", self.S_Stop))
        horizontalLayout.addWidget(self._GetButton("调试", "debug", self.S_Debug))
        horizontalLayout.addWidget(self._GetButton("下一步", "next", self.S_Next))
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontalLayout.addItem(spacerItem)

    def _GetButton(self, sName, sIcon, func):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/menu/%s.png" % sIcon), QIcon.Normal, QIcon.Off)
        oBtn = QPushButton(sName, self)
        oBtn.setIcon(icon)
        oBtn.setIconSize(QSize(30, 30))
        oBtn.clicked.connect(func)
        return oBtn

    def S_Save(self):
        pass

    def S_Start(self):
        pass

    def S_Stop(self):
        pass

    def S_Debug(self):
        pass

    def S_Next(self):
        pass
