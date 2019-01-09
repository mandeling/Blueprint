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
    def __init__(self, bpID, parent=None):
        super(CEventAttrTree, self).__init__(bpID, parent)

    def _LoadItem(self):
        lstVar = interface.GetBlueprintAttr(self.m_BPID, eddefine.BlueprintAttrName.VARIABLE_LIST)
        for varID in lstVar:
            self.m_ItemInfo[varID] = CTreeWidgetItem(varID, self)

class CEventAttrItem(basetree.CBaseAttrItem):
    m_AttrType = define.BP_ATTR_EVENT
    def __init__(self, ID, parent=None):
        super(CEventAttrItem, self).__init__(ID, parent)
        self.m_Name = interface.GetVariableAttr(varID, eddefine.VariableAttrName.NAME)
        self.m_Type = interface.GetVariableAttr(varID, eddefine.VariableAttrName.TYPE)