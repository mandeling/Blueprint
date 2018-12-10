# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 17:21:36
@Desc: 对editdata.interface的封装
"""

import editdata.define as eddefine
import bpdata.define as bddefine

from editdata import interface


def IsInputPin(bpID, nodeID, pinID):
    dAllInfo = interface.GetNodeAttr(bpID, nodeID, eddefine.NodeAttrName.PININFO)
    pinInfo = dAllInfo[pinID]
    iPinType = pinInfo[bddefine.PinAttrName.PIN_TYPE]
    if iPinType == bddefine.PIN_INPUT_TYPE:
        return True
    return False
