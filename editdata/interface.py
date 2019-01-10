# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 10:04:13
@Desc: 对ui层提供的接口
"""

import json
import re
import editdata.define as eddefine
import bpdata.define as bddefine

from .idmgr import GetIDMgr
from .nodemgr import GetNodeMgr
from .variablemgr import GetVariableMgr
from .linemgr import GetLineMgr
from .pinmgr import GetPinMgr
from .graphicmgr import GetGraphicMgr
from .bpmgr import GetBPMgr


# -----------------------蓝图-----------------------------
def NewBlueprint():
    bpID = GetBPMgr().NewBP()
    return bpID


def DelBlueprint(bpID):
    GetBPMgr().DelItem(bpID)


def GetBlueprintAttr(bpID, sAttrName):
    return GetBPMgr().GetItemAttr(bpID, sAttrName)


def SetBlueprintAttr(bpID, sAttrName, value):
    GetBPMgr().SetItemAttr(bpID, sAttrName, value)


def OpenBlueprint(sPath):
    with open(sPath, "r", encoding="utf-8") as f:
        dInfo = json.load(f)
        bpID = dInfo.pop(eddefine.BP_ATTR_NAME_PREFIX)
        GetBPMgr().LoadItemInfo(bpID, dInfo)
        return bpID


def SaveBlueprint(bpID, sPath):
    dInfo = GetBPMgr().GetItemSaveInfo(bpID)
    dInfo[eddefine.BP_ATTR_NAME_PREFIX] = bpID
    with open(sPath, "w", encoding="utf-8") as f:
        json.dump(dInfo, f, indent=4, ensure_ascii=False)


# -----------------------图表-----------------------------
def NewGraphic(bpID):
    graphicID = GetGraphicMgr().NewGraphic(bpID)
    return graphicID


def DelGraphic(graphicID):
    GetGraphicMgr().DelItem(graphicID)


def GetGraphicAttr(graphicID, sAttrName):
    return GetGraphicMgr().GetItemAttr(graphicID, sAttrName)


def GetGraphicIDByNodeID(nodeID):
    return GetIDMgr().GetGraphicByNode(nodeID)


# --------------------变量--------------------------------
def NewVariable(bpID):
    varID = GetVariableMgr().NewVariable(bpID)
    return varID


def DelVariable(varID):
    pass


def SetVariableAttr(varID, sAttrName, value):
    oVariableMgr = GetVariableMgr()
    oVariableMgr.SetItemAttr(varID, sAttrName, value)


def GetVariableAttr(varID, sAttrName):
    oVariableMgr = GetVariableMgr()
    return oVariableMgr.GetItemAttr(varID, sAttrName)


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


# ----------------------其他------------------------------
def GetSearchInfo(bpID, sTxt, bFuzzyMatch):
    if bFuzzyMatch:
        pattern = re.compile(sTxt)
    dGraphic = {}
    lstGraphic = GetBlueprintAttr(bpID, eddefine.BlueprintAttrName.GRAPHIC_LIST)
    for graphicID in lstGraphic:
        lstNode = GetGraphicAttr(graphicID, eddefine.GraphicAttrName.NODE_LIST)
        dNode = {}
        for nodeID in lstNode:
            lstPin = GetNodeAttr(nodeID, bddefine.NodeAttrName.PINIDLIST)
            resultPin = []
            for pinID in lstPin:
                pinName = GetPinAttr(pinID, bddefine.PinAttrName.DISPLAYNAME)
                if bFuzzyMatch:
                    if pattern.search(pinName):
                        resultPin.append(pinID)
                elif pinName == sTxt:
                    resultPin.append(pinID)
            if resultPin:
                dNode[nodeID] = resultPin
        if dNode:
            dGraphic[graphicID] = dNode
    return dGraphic
