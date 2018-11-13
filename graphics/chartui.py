
import weakref
from ui.BlueChartWidget import Ui_BlueChartWidget
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsTextItem, QWidget
from PyQt5.QtCore import Qt


class CBlueChartUI(QGraphicsProxyWidget):
    def __init__(self, oBlueChart, oScene, parent=None):
        super(CBlueChartUI, self).__init__(parent)
        self.m_BlueChart = weakref.ref(oBlueChart)
        self.m_Scene = weakref.ref(oScene)
        self.m_BlueChartWidget = CBlueChartWidget(oBlueChart)    # TODO
        # self.m_ChangeCharName = QGraphicsTextItem(self.m_BlueChartWidget.lb_Title.text(), self)
        # self.m_ChangeCharName.setTextInteractionFlags(Qt.IBeamCursor)


class CBlueChartWidget(Ui_BlueChartWidget, QWidget):
    def __init__(self, action, parent=None):
        super(CBlueChartWidget, self).__init__(parent)
        self.setupUi(self)
        self.m_Name = action.GetName()
        self.Init()
        self.InitSignal()
        self.show()

    def Init(self):
        self.lb_Title.setText(self.m_Name)
        self.btn_ShowProperty.setCursor(Qt.PointingHandCursor)
        self.btn_Source.hide()

    def InitSignal(self):
        self.btn_ShowProperty.clicked.connect(self.ShowProperty)

    def ShowProperty(self):
        pass
