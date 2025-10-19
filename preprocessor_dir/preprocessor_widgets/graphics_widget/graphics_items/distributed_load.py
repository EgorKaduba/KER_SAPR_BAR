from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QFont


class DistributedLoadItem(QGraphicsItem):
    def __init__(self, node_number: int, power: float, x_pos: float, bar_length: float, parent=None):
        super().__init__(parent)
        self.node_number = node_number
        self.power = power
        self.x_pos = x_pos
        self.bar_length = bar_length
        self.setPos(x_pos, 0)
        self.setZValue(5)

    def boundingRect(self):
        return QRectF(0, -30, self.bar_length, 40)

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.blue, 2))

        segment_count = max(3, int(self.bar_length / 30))
        segment_length = self.bar_length / segment_count

        if self.power > 0:  # Направление вправо
            for i in range(segment_count):
                x = i * segment_length + segment_length / 2
                painter.drawLine(x, 0, x, -20)
                painter.drawLine(x, -20, x - 4, -16)
                painter.drawLine(x, -20, x + 4, -16)
        else:  # Направление влево
            for i in range(segment_count):
                x = i * segment_length + segment_length / 2
                painter.drawLine(x, 0, x, -20)
                painter.drawLine(x, -20, x - 4, -24)
                painter.drawLine(x, -20, x + 4, -24)

        painter.setPen(QPen(Qt.darkBlue))
        font = QFont()
        font.setPointSize(7)
        font.setBold(True)
        painter.setFont(font)

        label = f"q={abs(self.power):.1f}"
        text_width = len(label) * 5
        text_x = self.bar_length / 2 - text_width / 2
        painter.drawText(text_x, -25, label)

    def update_length(self, new_length: float):
        """Обновляет длину распределенной нагрузки"""
        self.bar_length = new_length
        self.update()  # Принудительно перерисовываем