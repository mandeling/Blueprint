# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-11 22:29:45
@Desc: 蓝图运行
"""

import copy

from editdata import interface
from editdata import define as eddefine
from bpdata import define as bddefine


class CRunPinMgr:
    def __init__(self):
        self.m_ItemInfo = {}

    def RunOutputFlow(self, outputPin):
        lstline = interface.GetAllLineByPin(outputPin)
        for lineID in lstline:
            inputPin = interface.GetLineOtherPin(lineID, outputPin)
            self.RunInputFlow(inputPin)

    def RunInputFlow(self, inputPin):
        pass


def RunBlueprint(bpID):
    iEventNode = interface.GetBlueprintAttr(bpID, eddefine.BlueprintAttrName.EVENT_NODE)
    if not iEventNode:
        return
    lstPin = interface.GetNodeAttr(iEventNode, bddefine.NodeAttrName.PINIDLIST)
    startPin = lstPin[0]
    obj = CRunPinMgr()
    obj.RunOutputFlow(startPin)
    del obj
