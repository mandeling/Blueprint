# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-08 14:27:14
@Desc: 蓝图属性界面
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout,\
    QTreeWidget, QPushButton, QSpacerItem, QSizePolicy, \
    QTreeWidgetItem, QLabel
from . import variableui


class CExpandWidget(QWidget):
    def __init__(self, item, parent=None):
        super(CExpandWidget, self).__init__(parent)
        self._InitUI()
        self.m_Item = item

    def _InitUI(self):
        HBox = QHBoxLayout(self)
        foldBtn = QPushButton("fold", self)
        lable = QLabel("变量", self)
        item = QSpacerItem(67, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        addBtn = QPushButton("+", self)
        HBox.addWidget(foldBtn)
        HBox.addWidget(lable)
        HBox.addItem(item)
        HBox.addWidget(addBtn)

        foldBtn.clicked.connect(self.S_OnFold)

    def S_OnFold(self):
        if self.m_Item.isExpanded():
            self.m_Item.setExpanded(False)
        else:
            self.m_Item.setExpanded(True)


class CBPAttrWidget(QWidget):
    def __init__(self, bpID, parent=None):
        super(CBPAttrWidget, self).__init__(parent)
        self.m_TreeWidget = None
        self.m_BPID = bpID
        self._InitUI()
        self._InitVariableUI()

    def _InitUI(self):
        self.m_TreeWidget = QTreeWidget(self)
        self.m_TreeWidget.setHeaderHidden(True)
        vBox = QVBoxLayout(self)
        vBox.addWidget(self.m_TreeWidget)
        # vBox.addWidget(variableui.CVariableUI(self))
        self.setLayout(vBox)
        self.m_TreeWidget.setIndentation(0)

    def _InitVariableUI(self):
        self._AddHeadWidget(variableui.CVariableUI(self.m_BPID, self))

    def _AddHeadWidget(self, widget):
        item = QTreeWidgetItem()
        self.m_TreeWidget.addTopLevelItem(item)
        self.m_TreeWidget.setItemWidget(item, 0, CExpandWidget(item))

        section = QTreeWidgetItem(item)
        section.setDisabled(True)
        self.m_TreeWidget.setItemWidget(section, 0, widget)
        item.addChild(section)
