# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 17:43:07
@Desc: 节点引脚
"""

import copy
from . import define
from editdata import basemgr


class CPin(basemgr.CBase):
    def __init__(self, iPinType, iDataType, sName):
        super(CPin, self).__init__()
        self.m_Info = {
            define.PinAttrName.ID: -1,
            define.PinAttrName.NAME: sName,
            define.PinAttrName.DISPLAYNAME: sName,
            define.PinAttrName.PIN_TYPE: iPinType,
            define.PinAttrName.DATA_TYPE: -1,
            define.PinAttrName.VALUE: -1,
        }
        if iPinType in (define.PIN_INPUT_DATA_TYPE, define.PIN_OUTPUT_DATA_TYPE):
            self.m_Info[define.PinAttrName.DATA_TYPE] = iDataType
            self.m_Info[define.PinAttrName.VALUE] = define.GetDefauleValue(iDataType)

    def GetInfo(self):
        return copy.deepcopy(self.m_Info)
