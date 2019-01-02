# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 14:51:59
@Desc: 节点连线管理
"""

import misc

from signalmgr import GetSignal
from idmgr import GetIDMgr
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

    def NewLine(self, bpID, oPinID, iPinID):
        # 删除input槽之前的连接
        lstLine = GetIDMgr().GetAllLineByPin(iPinID)
        for lineID in lstLine:
            GetIDMgr().DelPinLine(oPinID, iPinID, lineID)
            GetSignal().DEL_LINE.emit(lineID)
        lineID = misc.uuid()
        oLine = CLine(lineID, oPinID, iPinID)
        self.m_Info[lineID] = oLine
        GetIDMgr().NewPinLine(oPinID, iPinID, lineID)
        GetIDMgr().AddLine2BP(bpID, lineID)
        return lineID

    def DelLine(self, lineID):
        oLine = self.m_Info[lineID]
        oPinID = oLine.GetAttr(define.LineAttrName.OUTPUT_PINID)
        iPinID = oLine.GetAttr(define.LineAttrName.INPUT_PINID)
        GetIDMgr().DelPinLine(oPinID, iPinID, lineID)
        GetIDMgr().DelLine(lineID)
        del self.m_Info[lineID]

    def SetLineAttr(self, lineID, sAttrName, value):
        oLine = self.m_Info[lineID]
        oLine.SetAttr(sAttrName, value)

    def GetLineAttr(self, lineID, sAttrName):
        oLine = self.m_Info[lineID]
        return oLine.GetAttr(sAttrName)


class CLine:
    def __init__(self, uid, oPinID, iPinID):
        self.m_Info = {
            define.LineAttrName.ID: uid,
            define.LineAttrName.OUTPUT_PINID: oPinID,
            define.LineAttrName.INPUT_PINID: iPinID,
        }

    def SetAttr(self, sAttrName, value):
        self.m_Info[sAttrName] = value

    def GetAttr(self, sAttrName):
        return self.m_Info[sAttrName]
