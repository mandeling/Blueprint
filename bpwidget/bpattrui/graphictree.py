# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-09 21:16:34
@Desc: 蓝图图表属性窗口
"""


from . import basetree
from .. import define
from editdata import interface
from editdata import define as eddefine
from signalmgr import GetSignal


class CGraphicAttrTree(basetree.CBaseAttrTree):
    m_BPAttrListName = eddefine.BlueprintAttrName.GRAPHIC_LIST

    def _New(self, ID):
        obj = CGraphicAttrItem(ID, self)
        return obj

    def _InitSignal(self):
        super(CGraphicAttrTree, self)._InitSignal()
        GetSignal().NEW_GRAPHIC.connect(self.S_NewItem)


class CGraphicAttrItem(basetree.CBaseAttrItem):
    m_AttrType = define.BP_ATTR_GRAPHIC

    def GetName(self):
        return interface.GetGraphicAttr(self.m_ID, eddefine.GraphicAttrName.NAME)
