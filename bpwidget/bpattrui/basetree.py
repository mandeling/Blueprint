# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-09 19:24:40
@Desc: 属性ui控件的基类
"""


from PyQt5.QtWidgets import QWidget, QHBoxLayout,\
    QTreeWidget, QPushButton, QSpacerItem, QSizePolicy, \
    QTreeWidgetItem, QLabel, QApplication

from PyQt5.QtGui import QIcon, QPixmap, QDrag, QPainter, QTextOption
from PyQt5.QtCore import QSize, Qt, QMimeData, QRectF
from signalmgr import GetSignal

from editdata import interface
from bpdata import define as bddefine
from editdata import define as eddefine
from .. import define


class CBPAttrMimeData(QMimeData):
    def __init__(self, parent=None):
        super(CBPAttrMimeData, self).__init__(parent)
        self.m_ItemInfo = None

    def SetItemInfo(self, tInfo):
        self.m_ItemInfo = tInfo

    def GetItemInfo(self):
        return self.m_ItemInfo


class CExpandWidget(QWidget):
    def __init__(self, item, sAttrType, bpID, parent=None):
        super(CExpandWidget, self).__init__(parent)
        self.m_Item = item
        self.m_BPID = bpID
        self.m_AttrType = sAttrType
        self.m_FoldBtn = None
        self._InitUI()

    def _InitUI(self):
        HBox = QHBoxLayout(self)
        self.m_FoldBtn = QPushButton(self)
        lable = QLabel(self.m_AttrType, self)
        item = QSpacerItem(67, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        addBtn = QPushButton("+", self)
        HBox.addWidget(self.m_FoldBtn)
        HBox.addWidget(lable)
        HBox.addItem(item)
        HBox.addWidget(addBtn)
        self.m_FoldBtn.clicked.connect(self.S_OnFold)
        addBtn.clicked.connect(self.S_OnAdd)
        self.SetExpanded(True)

    def S_OnFold(self):
        self.SetExpanded(not self.m_Item.isExpanded())

    def SetExpanded(self, bExpand):
        if bExpand:
            sIconName = ":/icon/unfold.png"
        else:
            sIconName = ":/icon/fold.png"
        self.m_Item.setExpanded(bExpand)
        icon = QIcon()
        icon.addPixmap(QPixmap(sIconName), QIcon.Normal, QIcon.Off)
        self.m_FoldBtn.setIcon(icon)
        self.m_FoldBtn.setIconSize(QSize(16, 16))

    def S_OnAdd(self):
        if self.m_AttrType == define.BP_ATTR_VARIABLE:
            interface.NewVariable(self.m_BPID)


class CBaseAttrTree(QTreeWidget):
    m_BPAttrListName = None

    def __init__(self, bpID, parent=None):
        super(CBaseAttrTree, self).__init__(parent)
        self.m_BPID = bpID
        self.m_ItemInfo = {}
        self.m_DragPosition = None
        self.setHeaderHidden(True)
        self._LoadItem()

    def _LoadItem(self):
        lstID = interface.GetBlueprintAttr(self.m_BPID, self.m_BPAttrListName)
        for ID in lstID:
            self.m_ItemInfo[ID] = self._New(ID)

    def _New(self, ID):
        raise Exception("未实现定义")

    def _InitSignal(self):
        pass

    def S_NewItem(self, bpID, ID):
        if bpID != self.m_BPID:
            return
        self.m_ItemInfo[ID] = self._New(ID)

    def mousePressEvent(self, event):
        super(CBaseAttrTree, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.m_DragPosition = event.pos()

    def mouseMoveEvent(self, event):
        super(CBaseAttrTree, self).mouseMoveEvent(event)
        if not self.m_DragPosition:
            return
        if (event.pos() - self.m_DragPosition).manhattanLength() < QApplication.startDragDistance():
            return
        oItem = self.currentItem()
        drag = QDrag(self)
        oMimeData = CBPAttrMimeData()
        oMimeData.SetItemInfo(oItem.GetInfo())
        drag.setMimeData(oMimeData)

        pixMap = QPixmap(120, 18)
        painter = QPainter(pixMap)
        painter.drawText(QRectF(0, 0, 120, 18), "drag", QTextOption(Qt.AlignVCenter))
        drag.setPixmap(pixMap)
        drag.exec(Qt.MoveAction)

    def mouseReleaseEvent(self, event):
        super(CBaseAttrTree, self).mouseReleaseEvent(event)
        self.m_DragPosition = None


class CBaseAttrItem(QTreeWidgetItem):
    m_AttrType = None

    def __init__(self, ID, parent=None):
        super(CBaseAttrItem, self).__init__(parent)
        self.m_ID = ID
        self.setFlags(self.flags() | Qt.ItemIsEditable)
        self.SetName()

    def GetName(self):
        return ""

    def SetName(self, sName=None):
        if not sName:
            sName = self.GetName()
        self.setText(0, self.m_Name)

    def GetInfo(self):
        return self.m_AttrType, self.m_ID
