# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-08 16:43:10
@Desc: 主函数
"""

import sys
import graphics
import misc

from ui import res_rc


def Start():
    sys.excepthook = misc.HandleException
    graphics.Show()


if __name__ == "__main__":
    Start()
