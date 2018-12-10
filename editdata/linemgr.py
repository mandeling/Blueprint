# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 14:51:59
@Desc: 节点连线管理
"""

from . import define

g_LineMgr = None


def GetLineMgr():
    global g_LineMgr
    if not g_LineMgr:
        g_LineMgr = CLineMgr()
    return g_LineMgr


class CLineMgr:
    def __init__(self):
        self.m_Info = {}

    def NewBlueprint(self, bpID):
        self.m_Info[bpID] = CBPLineMgr()

    def GetLine(self, bpID, lineID):
        oBpLine = self.m_Info[bpID]
        oLine = oBpLine.GetLine(lineID)

    def NewLine(self, bpID, oNodeID, oPinID, iNodeID, iPinID):
        oBpNode = self.m_Info[bpID]
        return oBpNode.NewNode(oNodeID, oPinID, iNodeID, iPinID)

    def DelLine(self, bpID, lineID):
        oBpNode = self.m_Info[bpID]
        oBpNode.DelLine(lineID)


class CBPLineMgr:
    def __init__(self):
        self.m_ID = 0
        self.m_Info = {}

    def NewID(self):
        self.m_ID += 1
        return self.m_ID

    def NewNode(self, oNodeID, oPinID, iNodeID, iPinID):
        uid = self.NewID()
        self.m_Info[uid] = CLine(uid, oNodeID, oPinID, iNodeID, iPinID)
        return uid

    def GetLine(self, lineID):
        return self.m_Info[lineID]

    def DelLine(self, lineID):
        del self.m_Info[lineID]


class CLine:
    def __init__(self, uid, oNodeID, oPinID, iNodeID, iPinID):
        self.m_Info = {
            define.LineAttrName.ID: uid,
            define.LineAttrName.OUTPUT_NODEID: oNodeID,
            define.LineAttrName.INPUT_NODEID: iNodeID,
            define.LineAttrName.OUTPUT_PINID: oPinID,
            define.LineAttrName.INPUT_PINID: iPinID,
        }
