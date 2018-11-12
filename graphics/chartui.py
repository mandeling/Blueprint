
from ui.BlueChartWidget import Ui_BlueChartWidget
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsTextItem
from PyQt5.QtCore import Qt


class CBlueChartUI(QGraphicsProxyWidget):
    def __init__(self, parent=None):
        super(CBlueChartUI, self).__init__(parent)
        self.m_BlueChartWidget = CBlueChartWidget(1)    # TODO
        self.m_BlueChartWidget.setupUi(self.m_BlueChartWidget)
        self.m_ChangeCharName = QGraphicsTextItem(self.m_BlueChartWidget.lb_Title.text(), self)
        self.m_ChangeCharName.setTextInteractionFlags(Qt.IBeamCursor)


class CBlueChartWidget(Ui_BlueChartWidget):
    def __init__(self, action, parent=None):
        super(CBlueChartWidget, self).__init__(parent)
        self.setupUi(self)
        self.Init()
        self.InitSignal()

    def Init(self):
        sName = "name"
        self.lb_Title.setText(sName)
        self.btn_ShowProperty.setCursor(Qt.PointingHandCursor)
        self.btn_Source.hide()

    def InitSignal(self):
        self.btn_ShowProperty.clicked.connect(self.ShowProperty)

    def ShowProperty(self):
        pass
