# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 10:04:13
@Desc: 对ui层提供的接口
"""

import json
import editdata.define as eddefine
import bpdata.define as bddefine

from .idmgr import GetIDMgr
from .nodemgr import GetNodeMgr
from .variablemgr import GetVariableMgr
from .linemgr import GetLineMgr
from .pinmgr import GetPinMgr
from .graphicmgr import GetGraphicMgr


# -----------------------图表-----------------------------
def NewGraphic():
    graphicID = GetGraphicMgr().NewItem()
    return graphicID


def OpenGraphic(sPath):
    with open(sPath, "r", encoding="utf-8") as f:
        dInfo = json.load(f)
        graphicID = dInfo.pop(eddefine.GRAPHIC_ATTR_NAME_PREFIX)
        GetGraphicMgr().LoadItemInfo(graphicID, dInfo)
        return graphicID


def SaveGraphic(graphicID, sPath):
    dInfo = GetGraphicMgr().GetItemSaveInfo(graphicID)
    with open(sPath, "w", encoding="utf-8") as f:
        json.dump(dInfo, f, indent=4, ensure_ascii=False)


def GetGraphicAttr(graphicID, sAttrName):
    return GetGraphicMgr().GetItemAttr(graphicID, sAttrName)


# --------------------变量--------------------------------
def GetVariableData():
    oVariableMgr = GetVariableMgr()
    return oVariableMgr.GetAllVarInfo()


def NewVariable(sName, iType=bddefine.Type.INT, value=None):
    oVariableMgr = GetVariableMgr()
    oVariableMgr.NewVariable(sName, iType, value)


def DelVariable(varID):
    pass


def SetVariableAttr(sName, sAttrName, value):
    oVariableMgr = GetVariableMgr()
    oVariableMgr.SetItemAttr(sName, sAttrName, value)


def GetVariableAttr(sName, sAttrName):
    oVariableMgr = GetVariableMgr()
    return oVariableMgr.GetItemAttr(sName, sAttrName)


# --------------------------节点--------------------------
def AddNode(graphicID, sName, pos=(0, 0)):
    """添加节点"""
    nodeID = GetNodeMgr().NewNode(graphicID, sName, pos)
    return nodeID


def DelNode(nodeID):
    GetNodeMgr().DelNode(nodeID)


def SetNodeAttr(nodeID, sAttrName, value):
    oNodeMgr = GetNodeMgr()
    oNodeMgr.SetItemAttr(nodeID, sAttrName, value)


def GetNodeAttr(nodeID, sAttrName):
    oNodeMgr = GetNodeMgr()
    return oNodeMgr.GetItemAttr(nodeID, sAttrName)


def GetAllDefineNodeName():
    oNodeMgr = GetNodeMgr()
    return oNodeMgr.GetAllDefineNodeName()


def GetNodeIDByPinID(pinID):
    return GetIDMgr().GetNodeByPin(pinID)


# ---------------------引脚-------------------------------
def AddPin(nodeID, oDefinePin):
    pinID = GetPinMgr().NewPin(oDefinePin)
    GetIDMgr().SetPin2Node(nodeID, pinID)
    return pinID


def DelPin(pinID):
    GetPinMgr().DelItem(pinID)
    GetIDMgr().DelPin2Node(pinID)


def GetPinAttr(pinID, sAttrName):
    return GetPinMgr().GetItemAttr(pinID, sAttrName)


def PinCanConnect(inputPinID, outputPinID):
    if inputPinID == outputPinID:
        return False
    inputNodeID = GetNodeIDByPinID(inputPinID)
    OutputNodeID = GetNodeIDByPinID(outputPinID)
    if inputNodeID == OutputNodeID:
        return False

    iPinType = GetPinAttr(inputPinID, bddefine.PinAttrName.PIN_TYPE)
    oPinType = GetPinAttr(outputPinID, bddefine.PinAttrName.PIN_TYPE)
    if iPinType == oPinType:    # 同为输入、输出引脚返回false
        return False
    if bddefine.PinIsFlow(iPinType) and bddefine.PinIsFlow(oPinType):   # 同为flow引脚
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


def GetLinePinInfo(lineID):
    iPinID = GetLineAttr(lineID, eddefine.LineAttrName.INPUT_PINID)
    oPinID = GetLineAttr(lineID, eddefine.LineAttrName.OUTPUT_PINID)
    return iPinID, oPinID


def GetLineOtherPin(lineID, pinID):
    """获取line下的另一个pinID"""
    iPinID, oPinID = GetLinePinInfo(lineID)
    if iPinID == pinID:
        return oPinID
    return iPinID


# ----------------------连线------------------------------
def AddLine(graphicID, oPinID, iPinID):
    """
    oNodeID：输出节点ID
    iNodeID：输入节点ID
    """
    lineID = GetLineMgr().NewLine(graphicID, oPinID, iPinID)
    return lineID


def DelLine(lineID):
    GetLineMgr().DelLine(lineID)


def GetLineAttr(lineID, sAttrName):
    oLineMgr = GetLineMgr()
    return oLineMgr.GetItemAttr(lineID, sAttrName)


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
