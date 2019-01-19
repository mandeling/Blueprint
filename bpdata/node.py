# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 17:01:07
@Desc: 蓝图节点定义
"""

import misc

from .import define, pin
from editdata import nodemgr
from editdata import basemgr
from run import bprun


def Register(sNodeName):
    def Cls(cls):
        obj = cls(-1, sNodeName)    # 定义节点的ID置为-1
        nodemgr.GetNodeMgr().Register(sNodeName, obj)
    return Cls


class CBaseNode(basemgr.CBase):
    m_NodeType = None

    def __init__(self, ID, sNodeName=None):
        super(CBaseNode, self).__init__(ID)
        assert self.m_NodeType is not None
        self.m_Info = {
            define.NodeAttrName.ID: ID,
            define.NodeAttrName.NAME: sNodeName,
            define.NodeAttrName.DISPLAYNAME: sNodeName,
            define.NodeAttrName.POSITION: (0, 0),
            define.NodeAttrName.PINIDLIST: [],
            define.NodeAttrName.TYPE: self.m_NodeType,
            define.NodeAttrName.VARIABLE_ID: 0,
        }
        self.m_FuncInfo = {}  # pin对应执行的函数
        self.m_PinInfo = {}
        self._Run()

    def SetID(self, ID):
        self.m_ID = ID
        self.SetAttr(define.NodeAttrName.ID, ID)

    def GetPinInfo(self):
        return self.m_PinInfo

    def GetFuncInfo(self):
        return self.m_FuncInfo

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
        # 更新pinInfo（pinName:真正的pin）
        for pinID in lstPin:
            pinName = GetPinMgr().GetItemAttr(pinID, define.PinAttrName.NAME)
            self.m_PinInfo[pinName] = GetPinMgr().GetItem(pinID)

    def _Run(self):
        lstInputFlow = self.InputFlow()
        lstOutputFlow = self.OutputFlow()
        lstInputData = self.InputData()
        lstOutputData = self.OutputData()
        for tmp in lstInputFlow:
            sPinName = tmp
            if isinstance(tmp, tuple):
                sPinName = tmp[0]
                self.m_FuncInfo[sPinName] = tmp[1]
            self.m_PinInfo[sPinName] = pin.CPin(-1, define.PIN_INPUT_FLOW_TYPE, 0, sPinName)

        for sPinName in lstOutputFlow:
            self.m_PinInfo[sPinName] = pin.CPin(-1, define.PIN_OUTPUT_FLOW_TYPE, 0, sPinName)

        for lst in lstInputData:
            sPinName, iDataType = lst[0], lst[1]
            value = None
            if len(lst) > 2:
                value = lst[2]
            self.m_PinInfo[sPinName] = pin.CPin(-1, define.PIN_INPUT_DATA_TYPE, iDataType, sPinName, value)

        for lst in lstOutputData:
            sPinName, iDataType = lst[0], lst[1]
            self.m_PinInfo[sPinName] = pin.CPin(-1, define.PIN_OUTPUT_DATA_TYPE, iDataType, sPinName)
            if len(lst) > 2:
                self.m_FuncInfo[sPinName] = lst[2]

    def GetValue(self, sPinName):
        oPin = self.m_PinInfo[sPinName]
        pinID = oPin.GetID()
        value = bprun.GetRunPinValue(pinID)
        return value

    def RunFlow(self, sPinName):
        oPin = self.m_PinInfo[sPinName]
        pinID = oPin.GetID()
        bprun.RunOutputFlow(pinID)

    def SetValue(self, sPinName, value):
        oPin = self.m_PinInfo[sPinName]
        pinID = oPin.GetID()
        bprun.SetRunPinValue(pinID, value)

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


# ------------------------------函数节点----------------------------------------
@Register(define.NodeName.ADD)
class CAdd(CBaseNode):
    m_NodeType = define.NODE_TYPE_FUNCTION

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
    m_NodeType = define.NODE_TYPE_FUNCTION

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
    m_NodeType = define.NODE_TYPE_FUNCTION

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
    m_NodeType = define.NODE_TYPE_FUNCTION

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


# -----------------------------事件节点-----------------------------------------
@Register(define.NodeName.START)
class CStart(CBaseNode):
    m_NodeType = define.NODE_TYPE_EVENT

    def OutputFlow(self):
        return ["输出"]


# -----------------------------变量节点-----------------------------------------
@Register(define.NodeName.GET_VARIABLE)
class CGetVariable(CBaseNode):
    m_NodeType = define.NODE_TYPE_VARIABLE

    def OutputData(self):
        return [
            ("输出", define.Type.INT),
        ]

    def Output1(self):
        return self.GetValue("输出")


@Register(define.NodeName.SET_VARIABLE)
class CSetVariable(CBaseNode):
    m_NodeType = define.NODE_TYPE_VARIABLE

    def InputFlow(self):
        return ["input"]

    def OutputFlow(self):
        return ["output"]

    def InputData(self):
        return [
            ("输入", define.Type.INT),
        ]

    def OutputData(self):
        return [
            ("输出", define.Type.INT, self.NodeFunc),
        ]

    def NodeFunc(self):
        # TODO set变量
        return self.GetValue("输入")


# -----------------------------流程节点-----------------------------------------
@Register(define.NodeName.PRINT)
class CPrint(CBaseNode):
    m_NodeType = define.NODE_TYPE_FLOW

    def InputFlow(self):
        return [("入口", self.NodeFunc)]

    def OutputFlow(self):
        return ["出口"]

    def InputData(self):
        return [
            ("值", define.Type.INT)
        ]

    def NodeFunc(self):
        misc.Info("打印结果:%s" % self.GetValue("值"))
        self.RunFlow("出口")


@Register(define.NodeName.IF)
class CIF(CBaseNode):
    m_NodeType = define.NODE_TYPE_FLOW

    def InputFlow(self):
        return [("入口", self.NodeFunc)]

    def OutputFlow(self):
        return ["True", "False"]

    def InputData(self):
        return [
            ("Condition", define.Type.BOOL),
        ]

    def NodeFunc(self):
        bTrue = self.GetValue("Condition")
        if bTrue:
            self.RunFlow("True")
        else:
            self.RunFlow("False")


@Register(define.NodeName.FOR)
class CFOR(CBaseNode):
    m_NodeType = define.NODE_TYPE_FLOW

    def InputFlow(self):
        return [("入口", self.NodeFunc)]

    def OutputFlow(self):
        return ["循环", "出口"]

    def InputData(self):
        return [
            ("Start", define.Type.INT),
            ("End", define.Type.INT),
            ("Step", define.Type.INT, 1),
        ]

    def OutputData(self):
        return [
            ("index", define.Type.INT),
        ]

    def NodeFunc(self):
        iStart = self.GetValue("Start")
        iEnd = self.GetValue("End")
        iStep = self.GetValue("Step")
        for i in range(iStart, iEnd, iStep):
            self.SetValue("index", i)
            self.RunFlow("循环")
        self.RunFlow("出口")
