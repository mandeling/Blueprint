# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-08 16:41:00
@Desc: 通用函数
"""

import sys
import traceback
import weakref
import types


def HandleException(execType, execValue, tb):
    if not tb:
        return
    msg = "".join(traceback.format_tb(tb))
    msg = msg + str(execValue) + "\n"
    while hasattr(tb, "tb_next"):
        tb = tb.tb_next
    msg += "%s\n" % tb.tb_frame.f_locals
    print(msg)


def PythonError():
    """打印栈信息"""
    msg = traceback.format_exc()
    tb = sys.exc_info()[-1]
    if not msg or not tb:
        return
    while tb.tb_next:
        tb = tb.tb_next
    msg += "%s\n" % tb.tb_frame.f_locals
    print(msg)


def IsBoundMethod(func):
    if not isinstance(func, types.MethodType):
        return False
    if not func.__self__:
        return False
    return True


class Functor(object):
    def __init__(self, func, *args):
        if IsBoundMethod(func):
            self._obj = weakref.ref(func.__self__)
            self._objdesc = str(func.__self__)
            self._func = func.__func__
        else:
            self._obj = func
            self._func = func
        self._args = args

    def __call__(self, *args):
        if not self._obj:
            return self._func(*(self._args + args))
        obj = self._obj()
        if not obj:
            raise Warning("实例对象已经被释放,引用:%s,绑定方法:%s" % (self._objdesc, self._func))
        return self._func(obj, *(self._args + args))
