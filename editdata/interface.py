# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 10:04:13
@Desc: 对ui层提供的接口
"""

import misc
import editdata.define as eddefine
import bpdata.define as bddefine

from . import nodemgr, variablemgr, linemgr, pinmgr, idmgr, bpmgr
from idmgr import GetIDMgr


# -----------------------蓝图-----------------------------
def NewBlueprint():
    bpID = bpmgr.GetBPMgr().NewBP()
    return bpID


def OpenBlueprint(sPath):
    bpID = misc.uuid()
    return bpID


def SaveBlueprint(bpID, sPath):
    pass


def GetBPIDByNodeID(nodeID):
    return GetIDMgr().GetBPIDByNodeID(nodeID)


# --------------------变量--------------------------------
def GetVariableData():
    oVariableMgr = variablemgr.GetVariableMgr()
    return oVariableMgr.GetAllVarInfo()


def NewVariable(sName, iType=bddefine.Type.INT, value=None):
    oVariableMgr = variablemgr.GetVariableMgr()
    oVariableMgr.NewVariable(sName, iType, value)


def SetVariableAttr(sName, sAttrName, value):
    oVariableMgr = variablemgr.GetVariableMgr()
    oVariableMgr.SetAttr(sName, sAttrName, value)


def GetVariableAttr(sName, sAttrName):
    oVariableMgr = variablemgr.GetVariableMgr()
    return oVariableMgr.GetAttr(sName, sAttrName)


# --------------------------节点--------------------------
def AddNode(bpID, sName, pos=(0, 0)):
    nodeID = nodemgr.GetNodeMgr().NewNode(bpID, sName, pos)
    return nodeID


def SetNodeAttr(nodeID, sAttrName, value):
    oNodeMgr = nodemgr.GetNodeMgr()
    oNodeMgr.SetNodeAttr(nodeID, sAttrName, value)


def GetNodeAttr(nodeID, sAttrName):
    oNodeMgr = nodemgr.GetNodeMgr()
    return oNodeMgr.GetNodeAttr(nodeID, sAttrName)


def GetAllDefineNodeName():
    oNodeMgr = nodemgr.GetNodeMgr()
    return oNodeMgr.GetAllDefineNodeName()


def DelNode(nodeID):
    oNodeMgr = nodemgr.GetNodeMgr()
    oNodeMgr.DelNode(nodeID)


def GetNodeIDByPinID(pinID):
    return GetIDMgr().GetNodeIDByPinID(pinID)


# ---------------------引脚-------------------------------
def GetPinAttr(pinID, sAttrName):
    oPinMgr = pinmgr.GetPinMgr()
    return oPinMgr.GetAttr(pinID, sAttrName)


def PinCanConnect(inputPinID, outputPinID):
    if inputPinID == outputPinID:
        return False
    inputNodeID = GetNodeIDByPinID(inputPinID)
    OutputNodeID = GetNodeIDByPinID(outputPinID)
    if inputNodeID == OutputNodeID:
        return False

    iPinType = GetPinAttr(inputPinID, bddefine.PinAttrName.PIN_TYPE)
    oPinType = GetPinAttr(outputPinID, bddefine.PinAttrName.PIN_TYPE)
    if bddefine.PinIsFlow(iPinType) and bddefine.PinIsFlow(oPinType):   # 同为flow引脚
        if iPinType == oPinType:    # 同为输入、输出引脚返回false
            return False
        return True

    if not (bddefine.PinIsFlow(iPinType) or bddefine.PinIsFlow(oPinType)):  # 同为数据引脚
        iDataType = GetPinAttr(inputPinID, bddefine.PinAttrName.DATA_TYPE)
        oDataType = GetPinAttr(outputPinID, bddefine.PinAttrName.DATA_TYPE)
        if iDataType == oDataType:  # 相同数据类型才可以连接
            return True
        return False

    return False


def IsInputPin(pinID):
    iPinType = GetPinAttr(pinID, bddefine.PinAttrName.PIN_TYPE)
    if bddefine.PinIsInput(iPinType):
        return True
    return False


def GetLineOtherPin(lineID, pinID):
    """获取line下的另一个pinID"""
    iPinID = GetLineAttr(lineID, eddefine.LineAttrName.INPUT_PINID)
    oPinID = GetLineAttr(lineID, eddefine.LineAttrName.OUTPUT_PINID)
    if iPinID == pinID:
        return oPinID
    return iPinID


# ----------------------连线------------------------------
def AddLine(bpID, oPinID, iPinID):
    """
    oNodeID：输出节点ID
    iNodeID：输入节点ID
    """
    lineID = linemgr.GetLineMgr().NewLine(bpID, oPinID, iPinID)
    return lineID


def DelLine(lineID):
    oLineMgr = linemgr.GetLineMgr()
    oLineMgr.DelLine(lineID)


def GetLineAttr(lineID, sAttrName):
    oLineMgr = linemgr.GetLineMgr()
    return oLineMgr.GetLineAttr(lineID, sAttrName)


def GetAllLineByNode(nodeID):
    """获取所有与node连接的lineID"""
    lstPin = GetNodeAttr(nodeID, bddefine.NodeAttrName.PINIDLIST)
    lstLine = set([])
    for pinID in lstPin:
        tmpLine = GetAllLineByPin(pinID)
        lstLine |= set(tmpLine)
    return lstLine


def GetAllLineByPin(pinID):
    """获取与pin相连的所有lineid"""
    return GetIDMgr().GetAllLineByPin(pinID)
