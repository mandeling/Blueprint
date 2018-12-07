# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 17:01:07
@Desc: 蓝图节点定义
"""

from .import define

g_NodeMgr = None


def GetNodeMgr():
    global g_NodeMgr
    if not g_NodeMgr:
        g_NodeMgr = CNodeManger()
    return g_NodeMgr


class CNodeManger:
    def __init__(self):
        self.m_NodeInfo = {}


class CBase:
    m_Name = ""

    def __init__(self):
        self.m_InputFlow = self.InputFlow()
        self.m_OutputFlow = self.OutputFlow()
        self.m_InputData = self.InputData()
        self.m_OutputData = self.OutputData()

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


class CAdd(CBase):
    m_Name = define.NodeName.ADD

    def InputData(self):
        return [
            (define.Type.INT, "输入1"),
            (define.Type.INT, "输入2"),
        ]

    def OutputData(self):
        return [
            (define.Type.INT, "输出"),
        ]

    def Output1(self):
        return 1
