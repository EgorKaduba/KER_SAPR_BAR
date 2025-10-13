from PyQt5.QtWidgets import QMenuBar, QMenu, QAction
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        QMenuBar.__init__(self, parent)
        self.parent = parent
        self.setup_menu_bar()

    def setup_menu_bar(self):
        file_menu = QMenu("&Файл", self)

        open_action = QAction(QIcon("images/open_icon.png"), "Открыть", file_menu)
        open_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_O))
        open_action.triggered.connect(self.open_file)  # noqa
        save_action = QAction(QIcon("images/save_icon.png"), "Сохранить", file_menu)
        save_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_S))
        save_action.triggered.connect(self.save_file)  # noqa
        exit_action = QAction(QIcon("images/exit_icon.png"), "Выход", file_menu)
        exit_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_C))
        exit_action.triggered.connect(self.parent.close)  # noqa

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        reference_menu = QMenu("Справка", self)

        manual_action = QAction(QIcon("images/manual_icon.png"), "Руководство", reference_menu)
        manual_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_I))
        manual_action.triggered.connect(self.open_manual)  # noqa

        reference_menu.addAction(manual_action)

        self.addMenu(file_menu)
        self.addMenu(reference_menu)

    def save_file(self):
        self.parent.status_bar.showMessage("Файл сохранён", msecs=3000)

    def open_file(self):
        filename = "test.json"
        self.parent.status_bar.showMessage(f"Файл {filename} открыт", msecs=3000)

    def open_manual(self):
        self.parent.status_bar.showMessage(f"Открыто руководство", msecs=0)