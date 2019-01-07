# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-01 16:32:54
@Desc: 变量
"""

import random
import copy
import misc

from . import define, basemgr
from bpdata import define as bddefine

g_VariableMgr = None


def GetVariableMgr():
    global g_VariableMgr
    if not g_VariableMgr:
        g_VariableMgr = CVariableMgr()
    return g_VariableMgr


class CVariableMgr(basemgr.CBaseMgr):
    def __init__(self):
        super(CVariableMgr, self).__init__()
        self.InitTestData()

    def NewVariable(self, sName, iType, value):
        if value is None:
            value = bddefine.GetDefauleValue(iType)
        varID = misc.uuid()
        self.m_ItemInfo[varID] = CVariable(varID, sName, iType, value)

    def InitTestData(self):
        for i in range(10):
            sName = "Test%s" % i
            iType = random.randint(1, 3)
            value = random.randint(-999999, 999999)
            self.NewVariable(sName, iType, value)

    def GetAllVarInfo(self):
        return copy.deepcopy(self.m_ItemInfo)

    # TODO
    # def SetAttr(self, varID, sAttrName, value):
    #     oData = self.m_ItemInfo[varID]
    #     oData.SetAttr(sAttrName, value)
    #     if sAttrName == define.VariableAttrName.NAME:
    #         self.m_ItemInfo[value] = oData
    #         del self.m_ItemInfo[varID]

    # def GetAttr(self, varID, sAttrName):
    #     oData = self.m_ItemInfo[varID]
    #     return oData.GetAttr(sAttrName)


class CVariable(basemgr.CBase):
    def __init__(self, varID, sName, iType, value):
        super(CVariable, self).__init__(varID)
        self.m_Info = {
            define.VariableAttrName.ID: varID,
            define.VariableAttrName.NAME: sName,
            define.VariableAttrName.TYPE: iType,
            define.VariableAttrName.VALUE: value
        }
