# -*- coding: utf-8 -*-

import os
import sys

lstIgnore = [".git", ".vscode", "__pycache__", "test", "log", "."]
lstPicSuffix = [".png", ".icon", ".jpg"]


def IsIgnore(sDir):
    for sTmp in lstIgnore:
        if sDir.find(sTmp) != -1:
            return True
    return False


def IsPic(sFile):
    for suffix in lstPicSuffix:
        if sFile.endswith(suffix):
            return True
    return False


def UI2PY():
    for sDir, _, lstFile in os.walk("."):
        for sFile in lstFile:
            if sFile.endswith(".ui"):
                sUIFile = os.path.join(sDir, sFile)
                sPYFile = sUIFile[:-3] + ".py"
                os.system("pyuic5 -o %s %s --from-imports" % (sPYFile, sUIFile))
                print("%s   ->    %s" % (sUIFile, sPYFile))


def GenerateQrcFile(sQrcFile):
    sQrc = "<RCC>\n"
    for sDir, _, lstFile in os.walk("."):
        sPrefix = os.path.split(sDir)[1]
        if IsIgnore(sPrefix):
            continue
        sQrc += '    <qresource prefix="%s">\n' % sPrefix
        for sFile in lstFile:
            if not IsPic(sFile):
                continue
            sFullFile = os.path.join(sDir, sFile)
            sQrc += '        <file>%s</file>\n' % sFullFile
        sQrc += '    </qresource>\n'
    sQrc += '</RCC>\n'
    with open(sQrcFile, "w", encoding="utf-8") as f:
        f.write(sQrc)


def QRC2PY():
    sQrcFile = "res.qrc"
    GenerateQrcFile(sQrcFile)
    sPyFile = sQrcFile[:-4] + "_rc.py"
    os.system("pyrcc5 -o %s %s" % (sPyFile, sQrcFile))
    print("%s   ->    %s" % (sQrcFile, sPyFile))


def QRC2PY2():
    for sDir, _, lstFile in os.walk("."):
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
