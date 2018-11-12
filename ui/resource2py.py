# -*- coding: utf-8 -*-

import os
import sys

lstIgnore = [".git", ".vscode", "__pycache__", "mytool", "log"]


def IsIgnore(sDir):
    for sTmp in lstIgnore:
        if sDir.find(sTmp) != -1:
            return True
    return False


def UI2PY():
    for sDir, _, lstFile in os.walk(os.getcwd()):
        if IsIgnore(sDir):
            continue
        for sFile in lstFile:
            if sFile.endswith(".ui"):
                sUIFile = os.path.join(sDir, sFile)
                sPYFile = sUIFile[:-3] + ".py"
                os.system("pyuic5 -o %s %s" % (sPYFile, sUIFile))
                print("%s   ->    %s" % (sUIFile, sPYFile))


def QRC2PY():
    for sDir, _, lstFile in os.walk(os.getcwd()):
        if IsIgnore(sDir):
            continue
        for sFile in lstFile:
            if sFile.endswith(".qrc"):
                sQrcFile = os.path.join(sDir, sFile)
                sPYFile = os.path.join(os.getcwd(), sFile)[:-4] + "_rc.py"
                sPYFile = sQrcFile[:-4] + "_rc.py"
                os.system("pyrcc5 -o %s %s" % (sPYFile, sQrcFile))
                print("%s   ->    %s" % (sQrcFile, sPYFile))


def Other2PY(sType):
    if sType in ("all", "ui"):
        UI2PY()
    if sType in ("all", "qrc"):
        QRC2PY()


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        Other2PY("all")
    else:
        Other2PY(sys.argv[1])
