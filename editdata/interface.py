# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 10:04:13
@Desc: 对ui层提供的接口
"""

from . import nodemgr, variablemgr, linemgr


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


# ---------------------引脚-------------------------------
def PinCanDrag(bpID, nodeID1, pinID1, nodeID2, pinID2):
    return True


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


def GetAllLineName(bpID, lineID):
    return []
# ----------------------------------------------------
