from PyQt5.QtWidgets import QGraphicsScene

from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.grid import GridItem
from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.bar import BarItem
from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.sealing import Sealing


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.add_grid()
        self.bars: list[BarItem] = list()
        self.last_x = -500
        self.left_sealing = Sealing(-501, -100, 200, "left")
        self.right_sealing = Sealing(-499, -100, 200, "right")
        self.addItem(self.left_sealing)
        self.addItem(self.right_sealing)
        self.left_sealing.hide()
        self.right_sealing.hide()

    def add_grid(self):
        grid = GridItem(20)
        self.addItem(grid)

    def add_bar(self, length: float = 1, height: float = 1):
        bar = BarItem(self.last_x, int(-height * 50), int(length * 100), int(height * 100))
        self.last_x += length * 100
        self.bars.append(bar)
        self.addItem(bar)
        self.right_sealing.setX(self.last_x + 1)

    def resize_bar(self, bar_id: int, new_length: float, new_height: float):
        if bar_id < 0 or bar_id >= len(self.bars):
            return
        bar = self.bars[bar_id]
        old_length = bar.rect().width()
        current_x = bar.rect().x()
        length_difference = int((new_length * 100) - old_length)
        bar.prepareGeometryChange()
        bar.setRect(current_x, int(-new_height * 50), int(new_length * 100), int(new_height * 100))
        for i in range(bar_id + 1, len(self.bars)):
            next_bar = self.bars[i]
            next_bar.prepareGeometryChange()
            next_bar.setX(next_bar.x() + length_difference)
        self.last_x += length_difference
        self.right_sealing.setX(self.last_x + 1)

    def remove_bar(self, bar_id: int):
        if bar_id < 0 or bar_id >= len(self.bars):
            return
        bar_to_remove = self.bars[bar_id]
        old_length = bar_to_remove.rect().width()
        self.removeItem(bar_to_remove)
        self.bars.pop(bar_id)
        for i in range(bar_id, len(self.bars)):
            next_bar = self.bars[i]
            next_bar.prepareGeometryChange()
            next_bar.setX(next_bar.x() - old_length)
        self.last_x -= old_length
        if not self.bars:
            self.last_x = -500
        self.right_sealing.setX(self.last_x + 1)

    def changed_left_sealing(self, visible: bool = True):
        self.left_sealing.setVisible(visible)

    def changed_right_sealing(self, visible: bool = True):
        self.right_sealing.setVisible(visible)
