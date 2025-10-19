import math
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen


class Sealing(QGraphicsItem):
    def __init__(self, x, y, height, side: str = "left", parent=None):
        super().__init__(parent)  # Используйте super() вместо QGraphicsItem.__init__
        self.height = height
        self.type = side
        self.setPos(x, y)

        # Упрощенные параметры
        self.line_length = 15  # Фиксированная длина
        self.line_spacing = 12  # Фиксированное расстояние

    def boundingRect(self):
        margin = self.line_length + 5
        if self.type == "left":
            return QRectF(-margin, 0, margin + 5, self.height + 1)
        else:
            return QRectF(-5, -1, margin + 5, self.height)

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(0, 0, 0, self.height)
        self.draw_simple_hatch_lines(painter)

    def draw_simple_hatch_lines(self, painter):
        num_lines = 20
        for i in range(num_lines):
            y = 0 + (i + 1) * (self.height / (num_lines + 1))
            if self.type == "left":
                end_point = QPointF(-self.line_length, y + self.line_length * 0.7)
            else:
                end_point = QPointF(self.line_length, y - self.line_length * 0.7)
            painter.drawLine(QPointF(0, y), end_point)
