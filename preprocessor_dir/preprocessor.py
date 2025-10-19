from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt

from preprocessor_dir.preprocessor_widgets.table_widget.table import Table
from preprocessor_dir.preprocessor_widgets.graphics_widget.graphics import Graphics


class Preprocessor(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setStyleSheet("background-color: #d5dbe3;")
        self.main_layout = QHBoxLayout(self)
        self.splitter = QSplitter(Qt.Vertical)
        self.bar_table = Table("bar", parent=self)
        self.concentrated_loads_table = Table("concentrated_loads", parent=self)
        self.distributed_loads_table = Table("distributed_loads", parent=self)
        self.graphics = Graphics()
        self.setup_ui()

    def setup_ui(self):
        self.splitter.addWidget(self.graphics)
        self.splitter.setChildrenCollapsible(False)

        tables_widget = QWidget()
        tables_layout = QHBoxLayout()
        tables_layout.addWidget(self.bar_table)
        tables_layout.addWidget(self.concentrated_loads_table)
        tables_layout.addWidget(self.distributed_loads_table)
        tables_layout.setContentsMargins(0, 0, 0, 0)
        tables_widget.setLayout(tables_layout)
        self.splitter.addWidget(tables_widget)

        self.splitter.setSizes([600, 300])
        self.main_layout.addWidget(self.splitter)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def get_all_info(self):
        bar_data = self.bar_table.get_info()
        concentrated_data = self.concentrated_loads_table.get_info()
        distributed_data = self.distributed_loads_table.get_info()
        if distributed_data is None:
            distributed_data = {
                "type": "distributed_loads",
                "count": 0,
                "info": []
            }
        if concentrated_data is None:
            concentrated_data = {
                "type": "concentrated_loads",
                "count": 0,
                "info": []
            }
        info = [
            bar_data,
            concentrated_data,
            distributed_data,
            {
                "type": "supports",
                "left_support": self.graphics.scene.left_sealing.isVisible(),
                "right_support": self.graphics.scene.right_sealing.isVisible()
            }
        ]
        return {"Objects": info}

    def filling_from_file(self, info: dict):
        self.graphics.scene.clear_all()
        self.bar_table.filling_from_file(info["Objects"][0])
        self.concentrated_loads_table.filling_from_file(info["Objects"][1])
        self.distributed_loads_table.filling_from_file(info["Objects"][2])
        if len(info["Objects"]) > 3 and info["Objects"][3]["type"] == "supports":
            supports_data = info["Objects"][3]
            left_support = supports_data.get("left_support", False)
            right_support = supports_data.get("right_support", False)
            self.graphics.scene.changed_left_sealing(left_support)
            self.graphics.scene.changed_right_sealing(right_support)
            self.graphics.set_supports_states(left_support, right_support)
        self.update_concentrated_loads_display()
        self.update_distributed_loads_display()

    def update_concentrated_loads_display(self):
        """Обновляет отображение сосредоточенных нагрузок на сцене"""
        self.graphics.scene.clear_concentrated_loads()
        if not self.graphics.scene.bars:
            return
        concentrated_data = self.concentrated_loads_table.get_info()
        if concentrated_data and concentrated_data["info"]:
            for load in concentrated_data["info"]:
                node_num = load.get("node_number")
                power = load.get("power")
                if node_num is not None and power is not None:
                    self.graphics.scene.add_concentrated_load(node_num, power)

    def update_loads_tables_after_bar_removal(self, removed_bar_id: int):
        """Обновляет таблицы нагрузок после удаления стержня"""
        concentrated_data = self.concentrated_loads_table.get_info()
        if concentrated_data and concentrated_data["info"]:
            new_concentrated_info = []
            for load in concentrated_data["info"]:
                node_num = load.get("node_number")
                if node_num == removed_bar_id + 2:
                    load["node_number"] = removed_bar_id + 1
                    new_concentrated_info.append(load)
                elif node_num > removed_bar_id + 2:
                    load["node_number"] = node_num - 1
                    new_concentrated_info.append(load)
                else:
                    new_concentrated_info.append(load)
            self.concentrated_loads_table.filling_from_file({
                "type": "concentrated_loads",
                "count": len(new_concentrated_info),
                "info": new_concentrated_info
            })

    def refresh_all_loads(self):
        """Полностью обновляет все нагрузки (используется при изменении стержней)"""
        self.update_concentrated_loads_display()
        self.update_concentrated_loads_display()
        self.update_distributed_loads_display()

    def update_distributed_loads_display(self):
        """Обновляет отображение распределенных нагрузок на сцене"""
        self.graphics.scene.clear_distributed_loads()
        if not self.graphics.scene.bars:
            return

        distributed_data = self.distributed_loads_table.get_info()
        if distributed_data and distributed_data["info"]:
            for load in distributed_data["info"]:
                bar_num = load.get("node_number") - 1
                power = load.get("power")
                if bar_num is not None and power is not None and 0 <= bar_num < len(self.graphics.scene.bars):
                    self.graphics.scene.add_distributed_load(bar_num, power)