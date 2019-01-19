# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-11 22:29:45
@Desc: 蓝图运行
"""

import misc

from editdata import interface
from editdata import define as eddefine
from bpdata import define as bddefine
from signalmgr import GetSignal


g_BlueprintRunMgr = None


def GetRunMgr():
    global g_BlueprintRunMgr
    if not g_BlueprintRunMgr:
        g_BlueprintRunMgr = CBlueprintRunMgr()
    return g_BlueprintRunMgr


# ---------------------ui层接口---------------------------
def RunBlueprint(bpID):
    """运行蓝图"""
    iEventNode = interface.GetBlueprintAttr(bpID, eddefine.BlueprintAttrName.EVENT_NODE)
    if not iEventNode:
        return
    lstPin = interface.GetNodeAttr(iEventNode, bddefine.NodeAttrName.PINIDLIST)
    startPin = lstPin[0]
    obj = GetRunMgr()
    obj.Run(startPin)


def StopBlueprint(bpID):
    """停止运行蓝图"""
    obj = GetRunMgr()
    obj.Reset()


def SetBreakpoint(nodeID):
    obj = GetRunMgr()
    bShow = obj.SetBreakpoint(nodeID)
    return bShow


def NextBreakpoint():
    obj = GetRunMgr()
    obj.NextBreakpoint()


# --------------------蓝图运行中的接口----------------------------
def GetRunPinValue(pinID):
    value = GetRunMgr().GetPinValue(pinID)
    return value


def RunOutputFlow(pinID):
    obj = GetRunMgr()
    obj.RunOutputFlow(pinID)


def SetRunPinValue(pinID, value):
    obj = GetRunMgr()
    obj.SetPinValue(pinID, value)


def GetPinFunc(pinID):
    nodeID = interface.GetNodeIDByPinID(pinID)
    pinName = interface.GetPinAttr(pinID, bddefine.PinAttrName.NAME)
    dFunc = interface.GetNodeFuncInfo(nodeID)
    func = dFunc.get(pinName, None)
    return func


BLUEPRINT_RUN = 1
BLUEPRINT_STOP = 2
BLUEPRINT_DEBUG = 4


def DebugPinInfo(pinID, value):
    nodeID = interface.GetNodeIDByPinID(pinID)
    sNodeDisplayName = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.DISPLAYNAME)
    sPinDisplayName = interface.GetPinAttr(pinID, bddefine.PinAttrName.DISPLAYNAME)
    misc.Debug("%s-%s: %s\t%s" % (sNodeDisplayName, sPinDisplayName, value, type(value)))


class CBlueprintRunMgr:
    def __init__(self):
        self.m_PinValue = {}
        self.m_Breakpoint = {}
        self.m_LineList = []
        self.m_CurInputFlowPin = None
        self.m_Statue = 0

    def Reset(self):
        self.m_PinValue = {}
        for lineID in self.m_LineList:
            GetSignal().LINE_RUN_STATUE.emit(lineID, False)
        self.m_LineList = []
        self.m_Statue = 0

    def _AddRunLine(self, lineID):
        if lineID not in self.m_LineList:
            self.m_LineList.append(lineID)
            GetSignal().LINE_RUN_STATUE.emit(lineID, True)

    def Run(self, startPin):
        self.Reset()
        self.m_Statue ^= BLUEPRINT_RUN
        self.RunOutputFlow(startPin)

    def SetPinValue(self, pinID, value):
        self.m_PinValue[pinID] = value

    def NextBreakpoint(self):
        if self.m_CurInputFlowPin:
            self.RunInputFlow(self.m_CurInputFlowPin)

    def SetBreakpoint(self, nodeID):
        if nodeID in self.m_Breakpoint:
            del self.m_Breakpoint[nodeID]
            return False
        self.m_Breakpoint[nodeID] = True
        return True

    def GetPinValue(self, pinID):
        if interface.IsFlowPin(pinID):
            misc.Error("flowpin:%s not value" % pinID)
            return

        if interface.IsInputPin(pinID):  # 输入引脚
            lstLine = interface.GetAllLineByPin(pinID)
            if lstLine:  # 有连线
                lineID = lstLine[0]
                outPin = interface.GetLineOtherPin(lineID, pinID)
                outPinValue = GetRunPinValue(outPin)
                self.m_PinValue[outPin] = outPinValue
                self.m_PinValue[pinID] = outPinValue

                DebugPinInfo(pinID, outPinValue)
                self._AddRunLine(lineID)
                return outPinValue

            # 无连线
            inputValue = interface.GetPinAttr(pinID, bddefine.PinAttrName.VALUE)
            self.m_PinValue[pinID] = inputValue
            DebugPinInfo(pinID, inputValue)
            return inputValue

        # 如果输入引脚有记录，那么直接返回值。
        # 而输入值可能随着输出值改变，所以需要获取
        if pinID in self.m_PinValue:
            return self.m_PinValue[pinID]

        # 输出引脚
        func = GetPinFunc(pinID)
        if func:
            outPinValue = func()
            self.m_PinValue[pinID] = outPinValue
            DebugPinInfo(pinID, outPinValue)
            return outPinValue

        outPinValue = interface.GetPinAttr(pinID, bddefine.PinAttrName.VALUE)
        self.m_PinValue[pinID] = outPinValue
        DebugPinInfo(pinID, outPinValue)
        return outPinValue

    def RunOutputFlow(self, outputPin):
        lstline = interface.GetAllLineByPin(outputPin)
        for lineID in lstline:
            inputPin = interface.GetLineOtherPin(lineID, outputPin)
            self.RunInputFlow(inputPin)
            self._AddRunLine(lineID)

    def RunInputFlow(self, inputPin):
        """输入流引脚永远只有一个"""
        nodeID = interface.GetNodeIDByPinID(inputPin)
        if self.m_CurInputFlowPin != inputPin and nodeID in self.m_Breakpoint:
            self.m_CurInputFlowPin = inputPin
            return
        func = GetPinFunc(inputPin)
        if func:
            sNodeDisplayName = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.DISPLAYNAME)
            misc.Debug("开始运行'%s'节点" % sNodeDisplayName)
            func()
            misc.Debug("'%s'节点运行完成" % sNodeDisplayName)
