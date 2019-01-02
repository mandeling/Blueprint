# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 14:51:59
@Desc: 节点连线管理
"""

from signalmgr import GetSignal
from . import define, pinmgr

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
        return oLine

    def NewLine(self, bpID, oNodeID, oPinID, iNodeID, iPinID):
        # 删除input槽之前的连接
        lstLine = pinmgr.GetPinMgr().GetAllLineByPin(bpID, iNodeID, iPinID)
        for lineID in lstLine:
            GetSignal().DEL_LINE.emit(lineID)

        oBpLine = self.m_Info[bpID]
        lineID = oBpLine.NewLine(oNodeID, oPinID, iNodeID, iPinID)
        oPinMgr = pinmgr.GetPinMgr()
        oPinMgr.NewLine(bpID, oNodeID, oPinID, iNodeID, iPinID, lineID)
        return lineID

    def DelPin(self, bpID, lineID):
        oLine = self.GetLine(bpID, lineID)
        dInfo = oLine.m_Info
        oNodeID = dInfo[define.LineAttrName.OUTPUT_NODEID]
        iNodeID = dInfo[define.LineAttrName.INPUT_NODEID]
        oPinID = dInfo[define.LineAttrName.OUTPUT_PINID]
        iPinID = dInfo[define.LineAttrName.INPUT_PINID]
        oPinMgr = pinmgr.GetPinMgr()
        oPinMgr.DelLine(bpID, oNodeID, oPinID, iNodeID, iPinID, lineID)

    def DelLine(self, bpID, lineID):
        self.DelPin(bpID, lineID)
        oBpLine = self.m_Info[bpID]
        oBpLine.DelLine(lineID)

    def SetLineAttr(self, bpID, lineID, sAttrName, value):
        oLine = self.GetLine(bpID, lineID)
        oLine.SetAttr(sAttrName, value)

    def GetLineAttr(self, bpID, lineID, sAttrName):
        oLine = self.GetLine(bpID, lineID)
        return oLine.GetAttr(sAttrName)


class CBPLineMgr:
    def __init__(self):
        self.m_ID = 0
        self.m_Info = {}

    def NewID(self):
        self.m_ID += 1
        return self.m_ID

    def NewLine(self, oNodeID, oPinID, iNodeID, iPinID):
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

    def SetAttr(self, sAttrName, value):
        self.m_Info[sAttrName] = value

    def GetAttr(self, sAttrName):
        return self.m_Info[sAttrName]
