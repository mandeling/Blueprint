# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-08 14:27:14
@Desc: 蓝图属性界面
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout,\
    QTreeWidget, QPushButton, QSpacerItem, QSizePolicy, \
    QTreeWidgetItem, QLabel

from .bpattrui import variabletree, graphictree
from . import define
from .bpattrui import basetree


class CBPAttrWidget(QWidget):
    def __init__(self, bpID, parent=None):
        super(CBPAttrWidget, self).__init__(parent)
        self.m_TreeWidget = None
        self.m_BPID = bpID
        self._InitUI()
        self._InitAttrUI()

    def _InitUI(self):
        self.m_TreeWidget = QTreeWidget(self)
        self.m_TreeWidget.setHeaderHidden(True)
        vBox = QVBoxLayout(self)
        vBox.addWidget(self.m_TreeWidget)
        self.setLayout(vBox)
        self.m_TreeWidget.setIndentation(0)

    def _InitAttrUI(self):
        for (sType, cls) in [
            (define.BP_ATTR_GRAPHIC, graphictree.CGraphicAttrTree),
            (define.BP_ATTR_VARIABLE, variabletree.CVariableAttrTree),
        ]:
            item = QTreeWidgetItem()
            self.m_TreeWidget.addTopLevelItem(item)
            oHeadWidget = basetree.CExpandWidget(item, sType, self.m_BPID)
            self.m_TreeWidget.setItemWidget(item, 0, oHeadWidget)

            section = QTreeWidgetItem(item)
            section.setDisabled(True)
            oWidget = cls(self.m_BPID, self)
            self.m_TreeWidget.setItemWidget(section, 0, oWidget)
            item.addChild(section)
