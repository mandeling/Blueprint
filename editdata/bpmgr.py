# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-29 10:02:06
@Desc: 蓝图管理类
"""

import misc

from . import define as eddefine

g_BPMgr = None


def GetBPMgr():
    global g_BPMgr
    if not g_BPMgr:
        g_BPMgr = CBPMgr()
    return g_BPMgr


class CBPMgr:
    def __init__(self):
        self.m_Info = {}

    def NewBP(self):
        uid = misc.uuid()
        oBP = CBP(uid, "name")
        self.m_Info[uid] = oBP
        return uid

    def DelBP(self, bpID):
        oBP = self.m_Info.get(bpID, None)
        if oBP:
            oBP.Delete()
            del self.m_Info[bpID]


class CBP:
    def __init__(self, ID, sName):
        self.m_Info = {
            eddefine.BlueprintAttrName.ID: ID,
            eddefine.BlueprintAttrName.NAME: sName,
            eddefine.BlueprintAttrName.LINE_LIST: [],
            eddefine.BlueprintAttrName.NODE_LIST: [],
            eddefine.BlueprintAttrName.VARIABLE_LIST: [],
        }

    def Delete(self):
        pass  # TODO
