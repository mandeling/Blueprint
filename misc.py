# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-08 16:41:00
@Desc: 通用函数
"""

from PyQt5.QtCore import QUuid


def uuid():
    sUid = QUuid().createUuid().toString()
    return sUid
