# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 17:01:07
@Desc: 蓝图节点定义
"""

from .import define, pin
from editdata import nodemgr
from editdata import basemgr


def Register(sNodeName):
    def Cls(cls):
        obj = cls(-1, sNodeName)    # 定义节点的ID置为-1
        nodemgr.GetNodeMgr().Register(sNodeName, obj)
    return Cls


class CBaseNode(basemgr.CBase):
    def __init__(self, ID, sNodeName=None):
        super(CBaseNode, self).__init__(ID)
        self.m_Info = {
            define.NodeAttrName.ID: ID,
            define.NodeAttrName.NAME: sNodeName,
            define.NodeAttrName.DISPLAYNAME: sNodeName,
            define.NodeAttrName.POSITION: (0, 0),
            define.NodeAttrName.PINIDLIST: [],
        }
        self.m_OutputFunc = {}  # 输出pin对应执行的函数
        self.m_PinInfo = {}
        self._Run()

    def SetID(self, ID):
        self.m_ID = ID
        self.SetAttr(define.NodeAttrName.ID, ID)

    def GetSaveInfo(self):
        from editdata.pinmgr import GetPinMgr
        dSaveInfo = super(CBaseNode, self).GetSaveInfo()
        lstPin = self.GetAttr(define.NodeAttrName.PINIDLIST)
        for pinID in lstPin:
            dTmp = GetPinMgr().GetItemSaveInfo(pinID)
            dSaveInfo.update(dTmp)
        return dSaveInfo

    def SetLoadInfo(self, dInfo):
        from editdata.pinmgr import GetPinMgr
        from editdata.idmgr import GetIDMgr
        super(CBaseNode, self).SetLoadInfo(dInfo)
        lstPin = self.GetAttr(define.NodeAttrName.PINIDLIST)
        for pinID in lstPin:
            GetPinMgr().LoadItemInfo(pinID, dInfo)
            GetIDMgr().SetPin2Node(self.m_ID, pinID)

    def _Run(self):
        lstInputFlow = self.InputFlow()
        lstOutputFlow = self.OutputFlow()
        lstInputData = self.InputData()
        lstOutputData = self.OutputData()
        for sPinName in lstInputFlow:
            self.m_PinInfo[sPinName] = pin.CPin(-1, define.PIN_INPUT_FLOW_TYPE, 0, sPinName)

        for sPinName in lstOutputFlow:
            self.m_PinInfo[sPinName] = pin.CPin(-1, define.PIN_OUTPUT_FLOW_TYPE, 0, sPinName)

        for lst in lstInputData:
            sPinName, iDataType = lst[0], lst[1]
            self.m_PinInfo[sPinName] = pin.CPin(-1, define.PIN_INPUT_DATA_TYPE, iDataType, sPinName)

        for lst in lstOutputData:
            sPinName, iDataType, func = lst[0], lst[1], lst[2]
            self.m_PinInfo[sPinName] = pin.CPin(-1, define.PIN_OUTPUT_DATA_TYPE, iDataType, sPinName)
            self.m_OutputFunc[sPinName] = func

    def GetValue(self, sPinName):
        oPin = self.m_PinInfo[sPinName]
        return oPin.GetAttr(define.PinAttrName.VALUE)

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


@Register(define.NodeName.ADD)
class CAdd(CBaseNode):
    def InputData(self):
        return [
            ("输入1", define.Type.INT),
            ("输入2", define.Type.INT),
        ]

    def OutputData(self):
        return [
            ("输出", define.Type.INT, self.Output1),
        ]

    def Output1(self):
        return self.GetValue("输入1") + self.GetValue("输入2")


@Register(define.NodeName.MIUNS)
class CMiuns(CBaseNode):
    def InputData(self):
        return [
            ("输入1", define.Type.INT),
            ("输入2", define.Type.INT),
        ]

    def OutputData(self):
        return [
            ("输出", define.Type.INT, self.Output1),
        ]

    def Output1(self):
        return self.GetValue("输入1") - self.GetValue("输入2")


@Register(define.NodeName.MULTIPLY)
class CMultipyl(CBaseNode):
    def InputData(self):
        return [
            ("输入1", define.Type.INT),
            ("输入2", define.Type.INT),
        ]

    def OutputData(self):
        return [
            ("输出", define.Type.INT, self.Output1),
        ]

    def Output1(self):
        return self.GetValue("输入1") * self.GetValue("输入2")


@Register(define.NodeName.DIVIDE)
class CDivide(CBaseNode):
    def InputData(self):
        return [
            ("输入1", define.Type.INT),
            ("输入2", define.Type.INT),
        ]

    def OutputData(self):
        return [
            ("输出", define.Type.INT, self.Output1),
        ]

    def Output1(self):
        return self.GetValue("输入1") / self.GetValue("输入2")


@Register(define.NodeName.PRINT)
class CPrint(CBaseNode):

    def InputData(self):
        return [
            ("输入1", define.Type.INT)
        ]

    def InputFlow(self):
        return ["输入"]

    def OutputFlow(self):
        return ["输出"]
