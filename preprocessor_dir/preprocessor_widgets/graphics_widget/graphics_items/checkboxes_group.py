from PyQt5.QtWidgets import QCheckBox, QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt


class CheckBoxGroup(QGroupBox):
    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)
        self.setTitle("Заделки")
        self.setAlignment(Qt.AlignHCenter)
        sealing_layout = QHBoxLayout(self)
        sealing_layout.setContentsMargins(0, 0, 0, 0)
        self.left_sealing = QCheckBox("Левая")
        self.left_sealing.setCheckState(0)
        self.left_sealing.toggled.connect(lambda checked: parent.scene.changed_left_sealing(checked))
        self.right_sealing = QCheckBox("Правая")
        self.right_sealing.setCheckState(0)
        self.right_sealing.toggled.connect(lambda checked: parent.scene.changed_right_sealing(checked))
        sealing_layout.addWidget(self.left_sealing)
        sealing_layout.addWidget(self.right_sealing)
        self.setLayout(sealing_layout)

    def set_states(self, left_visible, right_visible):
        """Устанавливает состояния чекбоксов"""
        self.left_sealing.blockSignals(True)
        self.right_sealing.blockSignals(True)
        self.left_sealing.setChecked(bool(left_visible))
        self.right_sealing.setChecked(bool(right_visible))
        self.left_sealing.blockSignals(False)
        self.right_sealing.blockSignals(False)
