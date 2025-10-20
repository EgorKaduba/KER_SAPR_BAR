from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene
from PyQt5.QtGui import QColor, QBrush, QPen, QFont
from PyQt5.QtCore import Qt, QRectF


class BarItem(QGraphicsRectItem):
    def __init__(self, x_pos: int = 0, y_pos: int = 0, length: int = 0, height: int = 0, parent: QGraphicsScene = None):
        super().__init__(x_pos, y_pos, length, height, parent)
        self.length = length
        self.height = height
        self.scene = parent
        self.real_length = length / 100.0
        self.real_height = height / 100.0
        self.setAcceptHoverEvents(True)
        self.modulus_elasticity = 0
        self.voltage = 0
        self.bar_number = 0
        self.setBrush(QBrush(QColor(255, 255, 255)))
        self.setPen(QColor(0, 0, 0))

    def boundingRect(self):
        original_rect = super().boundingRect()
        extra_height = 40
        return QRectF(original_rect.x(),
                     original_rect.y() - extra_height,
                     original_rect.width(),
                     original_rect.height() + extra_height)

    def set_properties(self, real_length: float, real_height: float, modulus_elasticity: float, voltage: float):
        self.real_length = real_length
        self.real_height = real_height
        self.modulus_elasticity = modulus_elasticity if modulus_elasticity is not None else 1.0
        self.voltage = voltage if voltage is not None else 1.0

    def set_bar_number(self, number: int):
        self.bar_number = number

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        self.draw_bar_number(painter)

    def draw_bar_number(self, painter):
        """Рисует номер стержня в кружочке посередине сверху"""
        center_x = self.rect().x() + self.rect().width() / 2
        top_y = self.rect().y()
        bar_number_str = str(self.bar_number)
        if len(bar_number_str) == 1:
            circle_radius = 12
        elif len(bar_number_str) == 2:
            circle_radius = 15
        else:
            circle_radius = 18
        circle_diameter = circle_radius * 2
        offset_from_bar = 8
        circle_rect = QRectF(center_x - circle_radius, top_y - circle_diameter - offset_from_bar,
                             circle_diameter, circle_diameter)
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(circle_rect)
        painter.setPen(QPen(Qt.black))
        font = QFont()
        if len(bar_number_str) == 1:
            font.setPointSize(9)
        elif len(bar_number_str) == 2:
            font.setPointSize(8)
        else:
            font.setPointSize(7)
        font.setBold(True)
        painter.setFont(font)
        text_rect = QRectF(center_x - circle_radius, top_y - circle_diameter - offset_from_bar,
                           circle_diameter, circle_diameter)
        painter.drawText(text_rect, Qt.AlignCenter, bar_number_str)

    def hoverEnterEvent(self, event):
        """Событие при наведении курсора"""
        self.setBrush(QBrush(QColor(180, 220, 255)))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """Событие при уходе курсора"""
        self.setBrush(QBrush(QColor(255, 255, 255)))
        super().hoverLeaveEvent(event)