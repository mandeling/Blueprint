
from PyQt5.QtCore import QUuid


def NewUuid():
    sUuid = QUuid().createUuid().toString()
    return sUuid
