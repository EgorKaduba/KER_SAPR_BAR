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
        self.display_scale = 100
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
        bar_width = int(display_length * self.display_scale)
        bar_height = int(display_height * self.display_scale)
        bar = BarItem(self.last_x, int(-bar_height / 2), bar_width, bar_height)
        bar.set_properties(length, height, modulus_elasticity, voltage)
        bar.set_bar_number(len(self.bars) + 1)
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
        new_width = display_length * self.display_scale
        new_height_px = display_height * self.display_scale

        bar.prepareGeometryChange()
        bar.setRect(current_x, -new_height_px / 2, new_width, new_height_px)

        if modulus_elasticity is not None:
            bar.modulus_elasticity = modulus_elasticity
        if voltage is not None:
            bar.voltage = voltage
        bar.real_length = new_length
        bar.real_height = new_height
        current_x = bar.rect().x() + new_width

        for i in range(bar_id + 1, len(self.bars)):
            next_bar = self.bars[i]
            next_bar.prepareGeometryChange()
            bar_width = next_bar.rect().width()
            bar_height = next_bar.rect().height()
            next_bar.setRect(current_x, -bar_height / 2, bar_width, bar_height)
            current_x += bar_width

        self.last_x = current_x
        self.right_sealing.setX(self.last_x)
        self.update_loads_positions()
        self.update_distributed_loads_positions()

    @staticmethod
    def _limit_length(length: float) -> float:
        return max(0.3, min(10.0, length))

    @staticmethod
    def _limit_height(height: float) -> float:
        return max(0.3, min(4.0, height))

    def remove_bar(self, bar_id: int):
        if bar_id < 0 or bar_id >= len(self.bars):
            return

        bar_to_remove = self.bars[bar_id]
        self.remove_bar_loads(bar_id)
        self.remove_distributed_load(bar_id)
        self.removeItem(bar_to_remove)
        self.bars.pop(bar_id)
        self.update_loads_node_numbers_after_removal(bar_id)
        self.update_distributed_loads_node_numbers_after_removal(bar_id)
        current_x = -500
        for i, bar in enumerate(self.bars):
            bar.prepareGeometryChange()
            current_width = bar.rect().width()
            current_height = bar.rect().height()
            bar.setRect(current_x, -current_height / 2, current_width, current_height)
            bar.set_bar_number(i + 1)
            current_x += current_width
        self.last_x = current_x
        self.right_sealing.setX(self.last_x)
        self.update_loads_positions()
        self.update_distributed_loads_positions()

    def remove_bar_loads(self, bar_id: int):
        pass

    def update_loads_node_numbers_after_removal(self, removed_bar_id: int):
        for load in self.concentrated_loads:
            if load.node_number == removed_bar_id + 2:
                load.node_number = removed_bar_id + 1
            elif load.node_number > removed_bar_id + 2:
                load.node_number -= 1

    def changed_left_sealing(self, visible: bool = True):
        self.left_sealing.setVisible(visible)

    def changed_right_sealing(self, visible: bool = True):
        self.right_sealing.setVisible(visible)

    def add_concentrated_load(self, node_number: int, power: float):
        if not self.bars:
            return

        x_pos = self.get_node_x_position(node_number)
        if x_pos is not None:
            load = ConcentratedLoadItem(node_number, power, x_pos)
            self.concentrated_loads.append(load)
            self.addItem(load)

    def get_node_x_position(self, node_number: int):
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
        for load in self.concentrated_loads:
            self.removeItem(load)
        self.concentrated_loads.clear()

    def update_loads_positions(self):
        for load in self.concentrated_loads:
            new_x = self.get_node_x_position(load.node_number)
            if new_x is not None:
                load.setPos(new_x, 0)

    def clear_all(self):
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

    def clear_distributed_loads(self):
        for load in self.distributed_loads:
            self.removeItem(load)
        self.distributed_loads.clear()

    def add_distributed_load(self, bar_id: int, power: float):
        if bar_id < 0 or bar_id >= len(self.bars):
            return
        bar = self.bars[bar_id]
        bar_rect = bar.rect()
        self.remove_distributed_load(bar_id)
        load = DistributedLoadItem(
            bar_id=bar_id,
            power=power,
            bar_start_x=bar_rect.x(),
            bar_length=bar_rect.width(),
            bar_height=bar_rect.height()
        )
        self.distributed_loads.append(load)
        self.addItem(load)

    def remove_distributed_load(self, bar_id: int):
        loads_to_remove = [load for load in self.distributed_loads if load.bar_id == bar_id]
        for load in loads_to_remove:
            self.removeItem(load)
            self.distributed_loads.remove(load)

    def update_distributed_loads_positions(self):
        for load in self.distributed_loads:
            if load.bar_id < len(self.bars):
                bar = self.bars[load.bar_id]
                bar_rect = bar.rect()
                load.update_position(bar_rect.x(), bar_rect.width(), bar_rect.height())

    def update_distributed_loads_node_numbers_after_removal(self, removed_bar_id: int):
        loads_to_remove = []
        loads_to_update = []
        for load in self.distributed_loads:
            if load.bar_id == removed_bar_id:
                loads_to_remove.append(load)
            elif load.bar_id > removed_bar_id:
                load.bar_id -= 1
                loads_to_update.append(load)
        for load in loads_to_remove:
            self.removeItem(load)
            self.distributed_loads.remove(load)
        for load in loads_to_update:
            if load.bar_id < len(self.bars):
                bar = self.bars[load.bar_id]
                bar_rect = bar.rect()
                load.update_position(bar_rect.x(), bar_rect.width(), bar_rect.height())
