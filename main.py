# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-08 16:43:10
@Desc: 
"""

import init
import sys
import graphics
import misc

def Start():
    sys.excepthook = misc.HandleException
    graphics.Show()


if __name__ == "__main__":
    Start()
