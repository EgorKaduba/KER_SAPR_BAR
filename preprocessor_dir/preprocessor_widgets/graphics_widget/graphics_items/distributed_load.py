from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QColor, QFont


class DistributedLoadItem(QGraphicsItem):
    def __init__(self, bar_id: int, power: float, bar_start_x: float, bar_length: float, bar_height: float,
                 parent=None):
        super().__init__(parent)
        self.bar_id = bar_id
        self.power = power
        self.bar_start_x = bar_start_x
        self.bar_length = bar_length
        self.bar_height = bar_height
        self.setZValue(5)
        self.setPos(bar_start_x, 0)

    def boundingRect(self):
        return QRectF(0, -15, self.bar_length, 30)

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.darkGreen, 2))
        min_arrow_spacing = 20
        max_arrows = 100
        arrow_count = min(max_arrows, int(self.bar_length / min_arrow_spacing))
        arrow_count = max(1, arrow_count)
        margin = 10
        available_length = self.bar_length - 2 * margin

        if arrow_count == 1:
            x_positions = [self.bar_length / 2]
        else:
            spacing = available_length / (arrow_count - 1)
            x_positions = [margin + i * spacing for i in range(arrow_count)]
        for x_pos in x_positions:
            x_pos_int = int(x_pos)
            if self.power > 0:
                arrow_length = min(8, int(available_length * 0.1))
                if x_pos_int + arrow_length <= self.bar_length:
                    painter.drawLine(x_pos_int, 0, x_pos_int + arrow_length, 0)
                    painter.drawLine(x_pos_int + arrow_length, 0, x_pos_int + arrow_length - 3, -3)
                    painter.drawLine(x_pos_int + arrow_length, 0, x_pos_int + arrow_length - 3, 3)
            else:
                arrow_length = min(8, int(available_length * 0.1))
                if x_pos_int - arrow_length >= 0:
                    painter.drawLine(x_pos_int, 0, x_pos_int - arrow_length, 0)
                    painter.drawLine(x_pos_int - arrow_length, 0, x_pos_int - arrow_length + 3, -3)
                    painter.drawLine(x_pos_int - arrow_length, 0, x_pos_int - arrow_length + 3, 3)
        painter.setPen(QPen(Qt.darkGreen))
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        painter.setFont(font)
        label = f"q={self.power:.1f}"
        text_width = 50
        text_height = 12
        text_x = int(self.bar_length / 2 - text_width / 2)
        text_y = 15
        if text_x < 5:
            text_x = 5
        elif text_x + text_width > self.bar_length - 5:
            text_x = int(self.bar_length - text_width - 5)
        painter.setPen(QPen(Qt.darkGreen))
        painter.drawText(text_x, text_y, label)

    def update_position(self, new_start_x: float, new_length: float, new_height: float):
        """Обновляет позицию при изменении стержня"""
        self.bar_start_x = new_start_x
        self.bar_length = new_length
        self.bar_height = new_height
        self.setPos(new_start_x, 0)
        self.update()