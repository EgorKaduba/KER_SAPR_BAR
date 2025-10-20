from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QFont


class ConcentratedLoadItem(QGraphicsItem):
    def __init__(self, node_number: int, power: float, x_pos: float, parent=None):
        super().__init__(parent)
        self.node_number = node_number
        self.power = power
        self.x_pos = x_pos
        self.setPos(x_pos, 0)
        self.setZValue(10)

    def boundingRect(self):
        return QRectF(-50, -25, 100, 50)

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.red, 2))
        if self.power > 0:
            painter.drawLine(0, 0, 35, 0)
            painter.drawLine(35, 0, 30, -5)
            painter.drawLine(35, 0, 30, 5)
        else:
            painter.drawLine(0, 0, -35, 0)
            painter.drawLine(-35, 0, -30, -5)
            painter.drawLine(-35, 0, -30, 5)
        painter.setPen(QPen(Qt.darkRed))
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        painter.setFont(font)
        label = f"{abs(self.power):.1f}"
        if self.power > 0:
            painter.drawText(5, -10, label)
        else:
            painter.drawText(-35, -10, label)