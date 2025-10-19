from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsView, QWidget, QHBoxLayout
from PyQt5.QtGui import QBrush, QWheelEvent, QPainter, QMouseEvent

from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_scene import GraphicsScene
from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.checkboxes_group import CheckBoxGroup


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

    def add_sealing_checkbox(self):
        checkbox_widget = QWidget(self)
        checkbox_widget.setStyleSheet("background-color: rgba(255,255,255,200);")

        layout = QHBoxLayout(checkbox_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.sealing_group = CheckBoxGroup(self)  # Сохраняем ссылку
        layout.addWidget(self.sealing_group)

        checkbox_widget.move(10, 380)
        checkbox_widget.resize(140, 50)

    def set_supports_states(self, left_visible, right_visible):
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
