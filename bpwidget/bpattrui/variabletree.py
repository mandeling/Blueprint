# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-09 19:30:59
@Desc: 事件TreeWidget
"""

from PyQt5.QtGui import QIcon, QPixmap

from . import basetree
from .. import define
from editdata import interface
from editdata import define as eddefine
from signalmgr import GetSignal


class CVariableAttrTree(basetree.CBaseAttrTree):
    m_BPAttrListName = eddefine.BlueprintAttrName.VARIABLE_LIST

    def _New(self, ID):
        obj = CVariableAttrItem(ID, self)
        return obj

    def _InitSignal(self):
        super(CVariableAttrTree, self)._InitSignal()
        GetSignal().NEW_VARIABLE.connect(self.S_NewItem)


class CVariableAttrItem(basetree.CBaseAttrItem):
    m_AttrType = define.BP_ATTR_VARIABLE

    def __init__(self, ID, parent=None):
        super(CVariableAttrItem, self).__init__(ID, parent)
        self._InitSignal()
        self.SetIcon()

    def _InitSignal(self):
        GetSignal().UI_VARIABLE_CHANGE_ATTR.connect(self.S_ChangeVarAttr)

    def GetName(self):
        return interface.GetVariableAttr(self.m_ID, eddefine.VariableAttrName.NAME)

    def GetType(self):
        return interface.GetVariableAttr(self.m_ID, eddefine.VariableAttrName.TYPE)

    def SetIcon(self, iType=None):
        if iType is None:
            iType = self.GetType()
        icon = QIcon()
        pix = ":/icon/btn_%s.png" % iType
        icon.addPixmap(QPixmap(pix), QIcon.Normal, QIcon.Off)
        self.setIcon(0, icon)

    def S_ChangeVarAttr(self, varID, attrName, value):
        if self.m_ID != varID:
            return
        interface.SetVariableAttr(varID, attrName, value)
        if attrName == eddefine.VariableAttrName.NAME:
            self.SetName(value)
        elif attrName == eddefine.VariableAttrName.TYPE:
            self.SetIcon(value)
