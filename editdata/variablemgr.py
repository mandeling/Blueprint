# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-01 16:32:54
@Desc: 变量
"""

import random
import copy

from . import define

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
        self.m_Data[sName] = CVariable(sName, iType, value)

    def InitTestData(self):
        for i in range(10):
            sName = "Test%s" % i
            dInfo = {
                "type": random.randint(0, 9),
                "value": random.randint(-999999, 999999)
            }
            self.m_Data[sName] = dInfo

    def GetAllVarInfo(self):
        return copy.deepcopy(self.m_Data)


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
