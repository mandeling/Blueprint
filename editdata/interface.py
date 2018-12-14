# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 10:04:13
@Desc: 对ui层提供的接口
"""

import editdata.define as eddefine
import bpdata.define as bddefine
from . import nodemgr, variablemgr, linemgr, pinmgr


g_BlueprintID = 0


# -----------------------蓝图-----------------------------
def NewBlueprint():
    global g_BlueprintID
    g_BlueprintID += 1
    nodemgr.GetNodeMgr().NewBlueprint(g_BlueprintID)
    linemgr.GetLineMgr().NewBlueprint(g_BlueprintID)
    return g_BlueprintID


def OpenBlueprint(sPath):
    global g_BlueprintID
    g_BlueprintID += 1
    # nodemgr.GetNodeMgr().NewBlueprint(g_BlueprintID)
    return g_BlueprintID


def SaveBlueprint(bpID, sPath):
    pass


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
def AddNode(bpID, sName):
    oNodeMgr = nodemgr.GetNodeMgr()
    return oNodeMgr.NewNode(bpID, sName)


def SetNodeAttr(bpID, nodeID, sAttrName, value):
    oNodeMgr = nodemgr.GetNodeMgr()
    oNodeMgr.SetNodeAttr(bpID, nodeID, sAttrName, value)


def GetNodeAttr(bpID, nodeID, sAttrName):
    oNodeMgr = nodemgr.GetNodeMgr()
    return oNodeMgr.GetNodeAttr(bpID, nodeID, sAttrName)


def GetAllDefineNodeName():
    oNodeMgr = nodemgr.GetNodeMgr()
    return oNodeMgr.GetAllDefineNodeName()


def DelNode(bpID, nodeID):
    oNodeMgr = nodemgr.GetNodeMgr()
    oNodeMgr.DelNode(bpID, nodeID)


# ---------------------引脚-------------------------------
def GetPinInfo(bpID, nodeID, pinID):
    dInfo = GetNodeAttr(bpID, nodeID, eddefine.NodeAttrName.PININFO)
    return dInfo[pinID]


def PinCanConnect(bpID, nodeID1, pinID1, nodeID2, pinID2):
    if nodeID1 == nodeID2:
        return False
    pinInfo1 = GetPinInfo(bpID, nodeID1, pinID1)
    pinInfo2 = GetPinInfo(bpID, nodeID2, pinID2)
    iPinTyp1 = pinInfo1[bddefine.PinAttrName.PIN_TYPE]
    iPinTyp2 = pinInfo2[bddefine.PinAttrName.PIN_TYPE]
    if iPinTyp1 == iPinTyp2:    # 同为输入、输出引脚
        return False
    iDataType1 = pinInfo1.get(bddefine.PinAttrName.DATA_TYPE, -1)
    iDataType2 = pinInfo2.get(bddefine.PinAttrName.DATA_TYPE, -1)
    if iDataType1 != iDataType2:    # 相同数据类型才可以连接
        return False
    return True


def IsInputPin(bpID, nodeID, pinID):
    pinInfo = GetPinInfo(bpID, nodeID, pinID)
    iPinType = pinInfo[bddefine.PinAttrName.PIN_TYPE]
    if iPinType == bddefine.PIN_INPUT_TYPE:
        return True
    return False


def GetAllPinByNode(bpID, nodeID):
    dInfo = GetNodeAttr(bpID, nodeID, eddefine.NodeAttrName.PININFO)
    lstPin = []
    for pinID in dInfo.keys():
        lstPin.append(pinID)
    return lstPin


# ----------------------连线------------------------------
def AddLine(bpID, oNodeID, oPinID, iNodeID, iPinID):
    """
    oNodeID：输出节点ID
    iNodeID：输入节点ID
    """
    oLineMgr = linemgr.GetLineMgr()
    return oLineMgr.NewLine(bpID, oNodeID, oPinID, iNodeID, iPinID)


def DelLine(bpID, lineID):
    oLineMgr = linemgr.GetLineMgr()
    oLineMgr.DelLine(bpID, lineID)


def GetAllLineByNode(bpID, nodeID):
    lstPin = GetAllPinByNode(bpID, nodeID)
    lstLine = set([])
    for pinID in lstPin:
        tmpLine = GetAllLineByPin(bpID, nodeID, pinID)
        lstLine |= set(tmpLine)
    return lstLine


# --------------------other--------------------------------
def GetAllLineByPin(bpID, nodeID, pinID):
    """获取与pin相连的所有lineid"""
    oPinMgr = pinmgr.GetPinMgr()
    return oPinMgr.GetAllLineByPin(bpID, nodeID, pinID)


def GetAllConnectPin(bpID, nodeID, pinID):
    """
    获取所有的与之相连的槽
    返回 [nodeID, pinID]
    """
    oPinMgr = pinmgr.GetPinMgr()
    return oPinMgr.GetAllConnectPin(bpID, nodeID, pinID)
