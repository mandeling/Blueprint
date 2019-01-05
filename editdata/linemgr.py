# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 14:51:59
@Desc: 节点连线管理
"""

import misc

from signalmgr import GetSignal
from .idmgr import GetIDMgr
from . import define, basemgr

g_LineMgr = None


def GetLineMgr():
    global g_LineMgr
    if not g_LineMgr:
        g_LineMgr = CLineMgr()
    return g_LineMgr


class CLineMgr(basemgr.CBaseMgr):

    def NewLine(self, bpID, oPinID, iPinID):
        # 删除input槽之前的连接
        lstLine = GetIDMgr().GetAllLineByPin(iPinID)
        for lineID in lstLine:
            self.DelLine(lineID)
            GetSignal().DEL_LINE.emit(bpID, lineID)
        lineID = misc.uuid()
        oLine = CLine(lineID, oPinID, iPinID)
        self.m_ItemInfo[lineID] = oLine
        GetIDMgr().NewPinLine(oPinID, iPinID, lineID)
        GetIDMgr().AddLine2BP(bpID, lineID)
        return lineID

    def DelLine(self, lineID):
        oLine = self.m_ItemInfo[lineID]
        oPinID = oLine.GetAttr(define.LineAttrName.OUTPUT_PINID)
        iPinID = oLine.GetAttr(define.LineAttrName.INPUT_PINID)
        GetIDMgr().DelPinLine(oPinID, iPinID, lineID)
        GetIDMgr().DelLine(lineID)
        del self.m_ItemInfo[lineID]


class CLine(basemgr.CBase):
    def __init__(self, uid, oPinID, iPinID):
        super(CLine, self).__init__()
        self.m_Info = {
            define.LineAttrName.ID: uid,
            define.LineAttrName.OUTPUT_PINID: oPinID,
            define.LineAttrName.INPUT_PINID: iPinID,
        }
