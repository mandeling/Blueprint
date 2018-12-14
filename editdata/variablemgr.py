# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-01 16:32:54
@Desc: 变量
"""

import random
import copy

from . import define
from bpdata import define as bddefine

g_VariableMgr = None


def GetVariableMgr():
    global g_VariableMgr
    if not g_VariableMgr:
        g_VariableMgr = CVariableMgr()
    return g_VariableMgr


class CVariableMgr:
    def __init__(self):
        self.m_Data = {}
        self.InitTestData()

    def NewVariable(self, sName, iType, value):
        if value is None:
            value = bddefine.GetDefauleValue(iType)
        self.m_Data[sName] = CVariable(sName, iType, value)

    def InitTestData(self):
        for i in range(10):
            sName = "Test%s" % i
            iType = random.randint(1, 3)
            value = random.randint(-999999, 999999)
            self.NewVariable(sName, iType, value)

    def GetAllVarInfo(self):
        return copy.deepcopy(self.m_Data)

    def SetAttr(self, sName, sAttrName, value):
        oData = self.m_Data[sName]
        oData.SetAttr(sAttrName, value)
        if sAttrName == define.VariableAttrName.NAME:
            self.m_Data[value] = oData
            del self.m_Data[sName]

    def GetAttr(self, sName, sAttrName):
        oData = self.m_Data[sName]
        return oData.GetAttr(sAttrName)


class CVariable:
    def __init__(self, sName, iType, value):
        self.m_Info = {
            define.VariableAttrName.NAME: sName,
            define.VariableAttrName.TYPE: iType,
            define.VariableAttrName.VALUE: value
        }

    def SetAttr(self, sAttrName, value):
        self.m_Info[sAttrName] = value

    def GetAttr(self, sAttrName):
        return self.m_Info[sAttrName]
