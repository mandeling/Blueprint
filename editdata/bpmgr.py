# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-29 10:02:06
@Desc: 蓝图管理类
"""

import misc

from . import basemgr
from . import define as eddefine

g_BPMgr = None


def GetBPMgr():
    global g_BPMgr
    if not g_BPMgr:
        g_BPMgr = CBPMgr()
    return g_BPMgr


class CBPMgr(basemgr.CBaseMgr):

    def NewItem(self):
        uid = misc.uuid()
        sName = "蓝图%s" % self.NewID()
        oBP = CBP(uid, sName)
        self.m_ItemInfo[uid] = oBP
        return uid

    def DelBP(self, bpID):
        oBP = self.m_ItemInfo.get(bpID, None)
        if oBP:
            oBP.Delete()
            del self.m_ItemInfo[bpID]


class CBP(basemgr.CBase):
    def __init__(self, ID, sName):
        super(CBP, self).__init__()
        self.m_Info = {
            eddefine.BlueprintAttrName.ID: ID,
            eddefine.BlueprintAttrName.NAME: sName,
            eddefine.BlueprintAttrName.LINE_LIST: [],
            eddefine.BlueprintAttrName.NODE_LIST: [],
            eddefine.BlueprintAttrName.VARIABLE_LIST: [],
        }

    def Delete(self):
        pass  # TODO
