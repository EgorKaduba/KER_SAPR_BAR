from PyQt5.QtWidgets import QGraphicsScene

from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.grid import GridItem
from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.bar import BarItem
from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.sealing import Sealing
from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.concentrated_load import ConcentratedLoadItem
from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics_items.distributed_load import DistributedLoadItem


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.add_grid()
        self.bars: list[BarItem] = list()
        self.concentrated_loads: list[ConcentratedLoadItem] = list()
        self.distributed_loads: list[DistributedLoadItem] = list()
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
        self.update_loads_positions()

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
        self.update_loads_positions()

    def changed_left_sealing(self, visible: bool = True):
        self.left_sealing.setVisible(visible)

    def changed_right_sealing(self, visible: bool = True):
        self.right_sealing.setVisible(visible)

    def add_concentrated_load(self, node_number: int, power: float):
        """Добавляет сосредоточенную нагрузку в указанный узел"""
        if not self.bars:  # Проверяем, есть ли стержни
            return

        x_pos = self.get_node_x_position(node_number)
        if x_pos is not None:
            load = ConcentratedLoadItem(node_number, power, x_pos)
            self.concentrated_loads.append(load)
            self.addItem(load)

    def get_node_x_position(self, node_number: int):
        """Возвращает X-координату узла (узлы нумеруются с 1)"""
        if not self.bars or node_number < 1 or node_number > len(self.bars) + 1:
            return None

        if node_number == 1:  # Левый конец первого стержня
            return self.bars[0].rect().x()
        elif node_number == len(self.bars) + 1:  # Правый конец последнего стержня
            bar = self.bars[-1]
            return bar.rect().x() + bar.rect().width()
        else:  # Узел между стержнями
            return self.bars[node_number - 1].rect().x()

    def clear_concentrated_loads(self):
        """Удаляет все сосредоточенные нагрузки со сцены"""
        for load in self.concentrated_loads:
            self.removeItem(load)
        self.concentrated_loads.clear()

    def add_distributed_load(self, node_number: int, power: float):
        """Добавляет распределенную нагрузку в указанный узел (начало стержня)"""
        bar_index = node_number - 1  # Узлы с 1, стержни с 0
        if 0 <= bar_index < len(self.bars):
            bar = self.bars[bar_index]
            x_pos = bar.rect().x()
            bar_length = bar.rect().width()
            load = DistributedLoadItem(node_number, power, x_pos, bar_length)
            self.distributed_loads.append(load)
            self.addItem(load)

    def clear_distributed_loads(self):
        """Удаляет все распределенные нагрузки со сцены"""
        for load in self.distributed_loads:
            self.removeItem(load)
        self.distributed_loads.clear()

    def update_loads_positions(self):
        """Обновляет позиции всех нагрузок при изменении стержней"""
        # Обновляем сосредоточенные нагрузки
        for load in self.concentrated_loads:
            new_x = self.get_node_x_position(load.node_number)
            if new_x is not None:
                load.setPos(new_x, 0)

        # Обновляем распределенные нагрузки
        for load in self.distributed_loads:
            bar_index = load.node_number - 1
            if 0 <= bar_index < len(self.bars):
                bar = self.bars[bar_index]
                new_x = bar.rect().x()
                new_length = bar.rect().width()
                load.setPos(new_x, 0)
                load.update_length(new_length)

    def clear_all(self):
        """Очищает все стержни и нагрузки со сцены"""
        left_visible = self.left_sealing.isVisible()
        right_visible = self.right_sealing.isVisible()

        for bar in self.bars:
            self.removeItem(bar)
        self.bars.clear()

        self.clear_concentrated_loads()
        self.clear_distributed_loads()  # Очищаем распределенные нагрузки

        self.last_x = -500
        self.right_sealing.setX(self.last_x + 1)
        self.left_sealing.setVisible(left_visible)
        self.right_sealing.setVisible(right_visible)
