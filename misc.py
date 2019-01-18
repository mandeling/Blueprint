# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-08 16:41:00
@Desc: 通用函数
"""

import logging

from PyQt5.QtCore import QUuid
from mainwidget.logwidget import GetLogWidget


def uuid():
    sUid = QUuid().createUuid().toString()
    return sUid


def Error(sMsg):
    logging.error(sMsg)
    GetLogWidget().AddLog(logging.ERROR, sMsg)


def Warn(sMsg):
    logging.warning(sMsg)
    GetLogWidget().AddLog(logging.WARN, sMsg)


def Info(sMsg):
    logging.info(sMsg)
    GetLogWidget().AddLog(logging.INFO, sMsg)


def Debug(sMsg):
    logging.debug(sMsg)
    GetLogWidget().AddLog(logging.DEBUG, sMsg)
