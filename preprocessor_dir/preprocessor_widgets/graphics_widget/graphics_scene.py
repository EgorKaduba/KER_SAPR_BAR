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

    def add_bar(self, length: float = 1, height: float = 1, modulus_elasticity: float = 1, voltage: float = 1):
        display_length = self._limit_length(length)
        display_height = self._limit_height(height)
        bar_width = display_length * 100
        bar_height = display_height * 100
        bar = BarItem(self.last_x, -bar_height / 2, bar_width, bar_height)
        bar.set_properties(length, height, modulus_elasticity, voltage)
        self.last_x += bar_width
        self.bars.append(bar)
        self.addItem(bar)
        self.right_sealing.setX(self.last_x)
        self.update_loads_positions()

    def resize_bar(self, bar_id: int, new_length: float, new_height: float, modulus_elasticity: float = None,
                   voltage: float = None):
        if bar_id < 0 or bar_id >= len(self.bars):
            return
        display_length = self._limit_length(new_length)
        display_height = self._limit_height(new_height)
        bar = self.bars[bar_id]
        old_width = bar.rect().width()
        current_x = bar.rect().x()
        new_width = display_length * 100
        new_height_px = display_height * 100
        width_difference = new_width - old_width
        bar.prepareGeometryChange()
        bar.setRect(current_x, -new_height_px / 2, new_width, new_height_px)
        if modulus_elasticity is not None:
            bar.modulus_elasticity = modulus_elasticity
        if voltage is not None:
            bar.voltage = voltage
        bar.real_length = new_length
        bar.real_height = new_height
        for i in range(bar_id + 1, len(self.bars)):
            next_bar = self.bars[i]
            next_bar.prepareGeometryChange()
            next_bar.setX(next_bar.x() + width_difference)
        self.last_x += width_difference
        self.right_sealing.setX(self.last_x)
        self.update_loads_positions()

    def _limit_length(self, length: float) -> float:
        """Ограничивает длину стержня для отображения"""
        return max(0.1, min(10.0, length))

    def _limit_height(self, height: float) -> float:
        """Ограничивает высоту стержня для отображения"""
        return max(0.1, min(4.0, height))

    def remove_bar(self, bar_id: int):
        if bar_id < 0 or bar_id >= len(self.bars):
            return
        bar_to_remove = self.bars[bar_id]
        old_width = bar_to_remove.rect().width()
        self.remove_bar_loads(bar_id)
        self.removeItem(bar_to_remove)
        self.bars.pop(bar_id)
        self.update_loads_node_numbers_after_removal(bar_id)
        current_x = self.bars[0].rect().x() if self.bars else -500
        for i, bar in enumerate(self.bars):
            if i == 0:
                continue
            bar.prepareGeometryChange()
            prev_bar = self.bars[i - 1]
            bar.setX(prev_bar.rect().x() + prev_bar.rect().width())
        if self.bars:
            last_bar = self.bars[-1]
            self.last_x = last_bar.rect().x() + last_bar.rect().width()
        else:
            self.last_x = -500

        self.right_sealing.setX(self.last_x)
        self.update_loads_positions()

    def remove_bar_loads(self, bar_id: int):
        """Удаляет все нагрузки, связанные с удаляемым стержнем"""
        loads_to_remove = []
        for load in self.concentrated_loads:
            if load.node_number == bar_id + 1 or load.node_number == bar_id + 2:
                loads_to_remove.append(load)
        for load in loads_to_remove:
            self.removeItem(load)
            self.concentrated_loads.remove(load)
        distributed_to_remove = []
        for load in self.distributed_loads:
            if load.node_number == bar_id + 1:
                distributed_to_remove.append(load)

        for load in distributed_to_remove:
            self.removeItem(load)
            self.distributed_loads.remove(load)

    def update_loads_node_numbers_after_removal(self, removed_bar_id: int):
        """Обновляет номера узлов у нагрузок после удаления стержня"""
        for load in self.concentrated_loads:
            if load.node_number > removed_bar_id + 1:
                load.node_number -= 1
        for load in self.distributed_loads:
            if load.node_number > removed_bar_id + 1:
                load.node_number -= 1

    def changed_left_sealing(self, visible: bool = True):
        self.left_sealing.setVisible(visible)

    def changed_right_sealing(self, visible: bool = True):
        self.right_sealing.setVisible(visible)

    def add_concentrated_load(self, node_number: int, power: float):
        """Добавляет сосредоточенную нагрузку в указанный узел"""
        if not self.bars:
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
        if node_number == 1:
            return self.bars[0].rect().x()
        elif node_number == len(self.bars) + 1:
            bar = self.bars[-1]
            return bar.rect().x() + bar.rect().width()
        else:
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
        for load in self.concentrated_loads:
            new_x = self.get_node_x_position(load.node_number)
            if new_x is not None:
                load.setPos(new_x, 0)
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
        self.clear_distributed_loads()
        self.last_x = -500
        self.right_sealing.setX(self.last_x + 1)
        self.left_sealing.setVisible(left_visible)
        self.right_sealing.setVisible(right_visible)