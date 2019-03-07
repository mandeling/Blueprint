# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-09 19:30:59
@Desc: 事件TreeWidget
"""

from . import basetree
from .. import define
from editdata import interface
from editdata import define as eddefine


class CEventAttrTree(basetree.CBaseAttrTree):
    m_BPAttrListName = ""

    def _New(self, ID):
        obj = CEventAttrItem(ID, self)
        return obj

    def _LoadItem(self):
        lstVar = interface.GetBlueprintAttr(self.m_BPID, eddefine.BlueprintAttrName.VARIABLE_LIST)
        for varID in lstVar:
            self.m_ItemInfo[varID] = CEventAttrItem(varID, self)


class CEventAttrItem(basetree.CBaseAttrItem):
    m_AttrType = define.BP_ATTR_EVENT

    def GetName(self):
        return ""
