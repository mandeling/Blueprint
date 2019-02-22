# -*- coding:utf-8 -*-
'''
@Author: lamborghini1993
@Date: 2019-01-11 22:29:45
@UpdateDate: 2019-02-22 16:13:39
@Description: 蓝图运行
'''

import misc
import threading
import time

from editdata import interface
from editdata import define as eddefine
from bpdata import define as bddefine
from signalmgr import GetSignal


g_BlueprintRun = None
g_BreakPoint = {}


def GetRunObj():
    global g_BlueprintRun
    # if not g_BlueprintRun:
    #     g_BlueprintRun = CBlueprintRun()
    return g_BlueprintRun


def InitRunObj():
    global g_BlueprintRun
    g_BlueprintRun = CBlueprintRun()
    return g_BlueprintRun


def RefreshObj():
    global g_BlueprintRun
    g_BlueprintRun = None


# ---------------------ui层接口---------------------------
def RunBlueprint(bpID):
    """运行蓝图"""
    obj = GetRunObj()
    if obj:
        obj.Stop()
        while obj.isAlive():
            time.sleep(0.5)
    iEventNode = interface.GetBlueprintAttr(bpID, eddefine.BlueprintAttrName.EVENT_NODE)
    if not iEventNode:
        return
    lstPin = interface.GetNodeAttr(iEventNode, bddefine.NodeAttrName.PINIDLIST)
    startPin = lstPin[0]
    obj = InitRunObj()
    obj.Run(startPin)


def StopBlueprint(bpID):
    """停止运行蓝图"""
    obj = GetRunObj()
    if obj:
        obj.Stop()


def NextBreakpoint():
    obj = GetRunObj()
    if obj:
        obj.NextBreakpoint()


def SetBreakpoint(nodeID):
    global g_BreakPoint
    if nodeID in g_BreakPoint:
        del g_BreakPoint[nodeID]
        return False
    g_BreakPoint[nodeID] = True
    return True


# --------------------蓝图运行中的接口----------------------------
def GetRunPinValue(pinID):
    value = GetRunObj().GetPinValue(pinID)
    return value


def RunOutputFlow(pinID):
    obj = GetRunObj()
    obj.RunOutputFlow(pinID)


def SetRunPinValue(pinID, value):
    obj = GetRunObj()
    obj.SetPinValue(pinID, value)


def GetPinFunc(pinID):
    nodeID = interface.GetNodeIDByPinID(pinID)
    pinName = interface.GetPinAttr(pinID, bddefine.PinAttrName.NAME)
    dFunc = interface.GetNodeFuncInfo(nodeID)
    func = dFunc.get(pinName, None)
    return func


BLUEPRINT_STOP = 1          # 停止
BLUEPRINT_RUNING = 2        # 运行中
BLUEPRINT_DEBUG_PAUSE = 4   # 调式中断等待中


def DebugPinInfo(pinID, value):
    nodeID = interface.GetNodeIDByPinID(pinID)
    sNodeDisplayName = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.DISPLAYNAME)
    sPinDisplayName = interface.GetPinAttr(pinID, bddefine.PinAttrName.DISPLAYNAME)
    misc.Debug("%s-%s: %s\t%s" % (sNodeDisplayName, sPinDisplayName, value, type(value)))


class CBlueprintRun(threading.Thread):
    def __init__(self):
        super(CBlueprintRun, self).__init__()
        self.m_StartPin = None
        self.m_PinValue = {}
        self.m_LineList = []
        self.m_Statue = 0
        self.setDaemon(True)

    def Stop(self):
        for lineID in self.m_LineList:
            GetSignal().LINE_RUN_STATUE.emit(lineID, False)
        self.m_Statue = BLUEPRINT_STOP

    def _AddRunLine(self, lineID):
        if lineID not in self.m_LineList:
            self.m_LineList.append(lineID)
            GetSignal().LINE_RUN_STATUE.emit(lineID, True)

    def Run(self, startPin):
        self.m_StartPin = startPin
        self.start()

    def run(self):
        misc.Debug("----------start----------")
        self.m_Statue = BLUEPRINT_RUNING
        self.RunOutputFlow(self.m_StartPin)

    def SetPinValue(self, pinID, value):
        self.m_PinValue[pinID] = value

    def NextBreakpoint(self):
        self.m_Statue = BLUEPRINT_RUNING

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
                # self.m_PinValue[outPin] = outPinValue
                # self.m_PinValue[pinID] = outPinValue

                DebugPinInfo(pinID, outPinValue)
                self._AddRunLine(lineID)
                return outPinValue

            # 无连线
            inputValue = interface.GetPinAttr(pinID, bddefine.PinAttrName.VALUE)
            # self.m_PinValue[pinID] = inputValue
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
            # self.m_PinValue[pinID] = outPinValue
            DebugPinInfo(pinID, outPinValue)
            return outPinValue

        outPinValue = interface.GetPinAttr(pinID, bddefine.PinAttrName.VALUE)
        # self.m_PinValue[pinID] = outPinValue
        DebugPinInfo(pinID, outPinValue)
        return outPinValue

    def RunOutputFlow(self, outputPin):
        if self.m_Statue == BLUEPRINT_STOP:
            return

        lstline = interface.GetAllLineByPin(outputPin)
        for lineID in lstline:
            inputPin = interface.GetLineOtherPin(lineID, outputPin)
            self.RunInputFlow(inputPin)
            self._AddRunLine(lineID)

    def RunInputFlow(self, inputPin, bNext=False):
        """输入流引脚永远只有一个"""
        if self.m_Statue & BLUEPRINT_STOP:
            return

        nodeID = interface.GetNodeIDByPinID(inputPin)
        if not bNext and nodeID in g_BreakPoint:
            self.m_Statue = BLUEPRINT_DEBUG_PAUSE
            while True:
                if self.m_Statue == BLUEPRINT_STOP:
                    return
                if self.m_Statue == BLUEPRINT_RUNING:
                    break
                time.sleep(0.5)

        func = GetPinFunc(inputPin)
        if func:
            sNodeDisplayName = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.DISPLAYNAME)
            misc.Debug("开始运行'%s'节点" % sNodeDisplayName)
            func()
