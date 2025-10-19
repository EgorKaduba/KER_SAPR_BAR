from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsView, QWidget, QHBoxLayout, QToolTip
from PyQt5.QtGui import QBrush, QWheelEvent, QPainter, QMouseEvent

from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_scene import GraphicsScene
from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.checkboxes_group import CheckBoxGroup
from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.bar import BarItem


class Graphics(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent=parent)
        self.setBackgroundBrush(QBrush(Qt.white))
        self.scene = GraphicsScene(parent=self)
        self.setScene(self.scene)
        self.setMinimumHeight(400)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet("QScrollBar { width: 0px; height: 0px; }")
        self.view_scale = 1
        self.add_sealing_checkbox()
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)

    def add_sealing_checkbox(self):
        self.checkbox_widget = QWidget(self)
        self.checkbox_widget.setStyleSheet("background-color: rgba(255,255,255,50);")
        self.checkbox_widget.setFixedSize(140, 50)
        layout = QHBoxLayout(self.checkbox_widget)
        layout.setContentsMargins(5, 5, 5, 5)
        self.sealing_group = CheckBoxGroup(self)
        layout.addWidget(self.sealing_group)
        self.update_checkbox_position()

    def update_checkbox_position(self):
        """Обновляет позицию чекбоксов при изменении размера"""
        margin = 10
        x = margin
        y = self.height() - self.checkbox_widget.height() - margin
        self.checkbox_widget.move(x, y)

    def resizeEvent(self, event):
        """Обрабатывает изменение размера окна"""
        super().resizeEvent(event)
        self.update_checkbox_position()

    def set_supports_states(self, left_visible, right_visible):
        """Устанавливает состояния чекбоксов заделок"""
        if hasattr(self, 'sealing_group'):
            self.sealing_group.set_states(left_visible, right_visible)

    def wheelEvent(self, event: QWheelEvent):
        zoom_factor = 1.15
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
            self.view_scale *= 1.15
        else:
            if self.view_scale >= 0.33:
                self.scale(1 / zoom_factor, 1 / zoom_factor)
                self.view_scale /= 1.15

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            fake_event = QMouseEvent(
                event.type(), event.localPos(), event.screenPos(),
                Qt.LeftButton, Qt.LeftButton, event.modifiers()
            )
            super().mousePressEvent(fake_event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.resetTransform()
            self.centerOn(0, 0)
            self.view_scale = 1
        else:
            super().keyPressEvent(event)

    def mouseMoveEvent(self, event):
        """Обрабатываем движение мыши для показа тултипов"""
        scene_pos = self.mapToScene(event.pos())
        items = self.scene.items(scene_pos)

        for item in items:
            if isinstance(item, BarItem):
                # Показываем тултип с информацией о стержне
                tooltip_text = (f"Стержень\n"
                                f"Длина: {item.real_length:.3f} м\n"
                                f"Сечение: {item.real_height:.3f} м²\n"
                                f"Модуль упругости: {item.modulus_elasticity:.0f} Па\n"
                                f"Допускаемое напряжение: {item.voltage:.0f} Па")
                QToolTip.showText(event.globalPos(), tooltip_text, self)
                break
        else:
            QToolTip.hideText()

        super().mouseMoveEvent(event)