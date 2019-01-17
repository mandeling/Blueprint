# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-11 22:29:45
@Desc: 蓝图运行
"""

import copy
import logging

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


def GetPinValue(pinID):
    value = GetRunMgr().GetPinValue(pinID)
    return value


def GetPinFunc(pinID):
    nodeID = interface.GetNodeIDByPinID(pinID)
    pinName = interface.GetPinAttr(pinID, bddefine.PinAttrName.NAME)
    dFunc = interface.GetNodeFuncInfo(nodeID)
    func = dFunc.get(pinName, None)
    return func


BLUEPRINT_RUN = 1
BLUEPRINT_STOP = 2
BLUEPRINT_DEBUG = 4


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

    def Run(self, startPin):
        self.Reset()
        self.m_Statue ^= BLUEPRINT_RUN
        self.RunOutputFlow(startPin)

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
            logging.error("flowpin:%s not value" % pinID)
            return
        if pinID in self.m_PinValue:
            return self.m_PinValue[pinID]

        if interface.IsInputPin(pinID):  # 输入引脚
            lstLine = interface.GetAllLineByPin(pinID)
            if lstLine:  # 有连线
                lineID = lstLine[0]
                outPin = interface.GetLineOtherPin(lineID, pinID)
                outPinValue = GetPinValue(outPin)
                self.m_PinValue[outPin] = outPinValue
                self.m_PinValue[pinID] = outPinValue
                logging.info("pin:%s->%s value:%s type:%s" % (outPin, pinID, outPinValue, type(outPinValue)))
                GetSignal().LINE_RUN_STATUE.emit(lineID, True)
                self.m_LineList.append(lineID)
                return outPinValue

            # 无连线
            inputValue = interface.GetPinAttr(pinID, bddefine.PinAttrName.VALUE)
            self.m_PinValue[pinID] = inputValue
            logging.info("pin:%s value:%s type:%s" % (pinID, inputValue, type(inputValue)))
            return inputValue

        # 输出引脚
        func = GetPinFunc(pinID)
        if func:
            outPinValue = func()
            self.m_PinValue[pinID] = outPinValue
            logging.info("pin:%s value:%s type:%s" % (pinID, outPinValue, type(outPinValue)))
            return outPinValue

        outPinValue = interface.GetPinAttr(pinID, bddefine.PinAttrName.VALUE)
        self.m_PinValue[pinID] = outPinValue
        logging.info("pin:%s value:%s type:%s" % (pinID, outPinValue, type(outPinValue)))
        return outPinValue

    def RunOutputFlow(self, outputPin):
        lstline = interface.GetAllLineByPin(outputPin)
        for lineID in lstline:
            inputPin = interface.GetLineOtherPin(lineID, outputPin)
            self.RunInputFlow(inputPin)
            GetSignal().LINE_RUN_STATUE.emit(lineID, True)
            self.m_LineList.append(lineID)

    def RunInputFlow(self, inputPin):
        nodeID = interface.GetNodeIDByPinID(inputPin)
        if self.m_CurInputFlowPin != inputPin and nodeID in self.m_Breakpoint:
            self.m_CurInputFlowPin = inputPin
            return
        func = GetPinFunc(inputPin)
        if func:
            func()
        lstPin = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.PINIDLIST)
        for pinID in lstPin:
            if pinID == inputPin:
                continue
            iType = interface.GetPinAttr(pinID, bddefine.PinAttrName.PIN_TYPE)
            if iType != bddefine.PIN_OUTPUT_FLOW_TYPE:
                continue
            self.RunOutputFlow(pinID)
