# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-01 16:32:54
@Desc: 变量
"""

import random
import copy
import misc

from .idmgr import GetIDMgr
from . import define, basemgr
from . import define as eddefine
from bpdata import define as bddefine
from signalmgr import GetSignal

g_VariableMgr = None


def GetVariableMgr():
    global g_VariableMgr
    if not g_VariableMgr:
        g_VariableMgr = CVariableMgr()
    return g_VariableMgr


class CVariableMgr(basemgr.CBaseMgr):

    def NewVariable(self, bpID):
        from .bpmgr import GetBPMgr
        iType = bddefine.Type.INT
        sName = "NewVar%s" % self.NewID()
        varID = misc.uuid()
        self.m_ItemInfo[varID] = CVariable(varID, sName, iType, 0)
        GetIDMgr().SetVar2BP(bpID, varID)
        GetBPMgr().AddToAttrList(bpID, eddefine.BlueprintAttrName.VARIABLE_LIST, varID)
        GetSignal().NEW_VARIABLE.emit(bpID, varID)
        return varID

    def NewObj(self, ID):
        obj = CVariable(ID)
        return obj


class CVariable(basemgr.CBase):
    def __init__(self, varID, sName=None, iType=None, value=None):
        super(CVariable, self).__init__(varID)
        self.m_Info = {
            define.VariableAttrName.ID: varID,
            define.VariableAttrName.NAME: sName,
            define.VariableAttrName.TYPE: iType,
            define.VariableAttrName.VALUE: value
        }
