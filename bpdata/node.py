# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 17:01:07
@Desc: 蓝图节点定义
"""

from .import define, pin
from editdata import nodemgr


def Register(sNodeName):
    def Cls(cls):
        cls(sNodeName)
    return Cls


class CBase:
    def __init__(self, sNodeName):
        self.m_NodeName = sNodeName
        self.m_InputFlow = self.InputFlow()
        self.m_OutputFlow = self.OutputFlow()
        self.m_InputData = self.InputData()
        self.m_OutputData = self.OutputData()
        self.m_ID = 0
        self.m_InputMap = {}    # 输入的映射
        self.m_OutputFunc = {}  # 输出pin对应执行的函数
        self.m_PinInfo = {}
        self.Init()
        self.Register()

    def InputFlow(self):
        """输入流引脚的定义"""
        return []

    def OutputFlow(self):
        """输出流引脚的定义"""
        return []

    def InputData(self):
        """输入数据引脚的定义"""
        return []

    def OutputData(self):
        """输出数据引脚的定义"""
        return []

    def NewID(self):
        self.m_ID += 1
        return self.m_ID

    def Init(self):
        for sName in self.m_InputFlow:
            pid = self.NewID()
            oPin = pin.CFlowPin(pid, define.PIN_INPUT_TYPE, sName)
            self.m_PinInfo[pid] = oPin.GetInfo()

        for sName in self.m_OutputFlow:
            pid = self.NewID()
            oPin = pin.CFlowPin(pid, define.PIN_OUTPUT_TYPE, sName)
            self.m_PinInfo[pid] = oPin.GetInfo()

        iInputID = 0
        for lst in self.m_InputData:
            iDataType, sName = lst[0], lst[1]
            pid = self.NewID()
            oPin = pin.CDataPin(pid, define.PIN_INPUT_TYPE, iDataType, sName)
            self.m_PinInfo[pid] = oPin.GetInfo()
            iInputID += 1
            nodemgr.GetNodeMgr().BindInputID(self.m_NodeName, iInputID, pid)

        for lst in self.m_OutputData:
            iDataType, sName, func = lst[0], lst[1], lst[2]
            pid = self.NewID()
            oPin = pin.CDataPin(pid, define.PIN_OUTPUT_TYPE, iDataType, sName)
            self.m_PinInfo[pid] = oPin.GetInfo()
            self.m_OutputFunc[pid] = func

    def GetValue(self, iInputID):
        return nodemgr.GetNodeMgr().GetValue(self.m_NodeName, iInputID)

    def Register(self):
        nodemgr.GetNodeMgr().Register(self.m_NodeName, self.m_PinInfo)


@Register(define.NodeName.ADD)
class CAdd(CBase):
    def InputData(self):
        return [
            (define.Type.INT, "输入1"),
            (define.Type.INT, "输入2"),
        ]

    def OutputData(self):
        return [
            (define.Type.INT, "输出", self.Output1),
        ]

    def Output1(self):
        return self.GetValue(0) + self.GetValue(1)


@Register(define.NodeName.PRINT)
class CPrint(CBase):

    def InputFlow(self):
        return ["输入"]

    def OutputFlow(self):
        return ["输出"]
