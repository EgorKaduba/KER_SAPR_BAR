import json

from PyQt5.QtWidgets import QMenuBar, QMenu, QAction
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt

from widgets.fileDialog import FileDialog
from widgets.manual import Manual

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
        if not self.parent.file_path:
            dialog = FileDialog(dialog_type="save")
            if dialog.file_path:
                open(dialog.file_path, "a").close()
                info = self.parent.get_all_info()
                if all(info["Objects"]):
                    try:
                        with open(dialog.file_path, "w") as file:
                            json_data = json.dumps(info)
                            file.write(json_data)
                        self.parent.status_bar.showMessage(f"Файл {dialog.file_path} сохранён", msecs=4000)
                    except Exception as error_msg:
                        self.parent.status_bar.showMessage(f"{error_msg}", msecs=4000)
            else:
                self.parent.status_bar.showMessage(f"Ошибка сохранения файла", msecs=4000)

    def open_file(self):
        dialog = FileDialog(dialog_type="open")
        if dialog.file_path:
            self.parent.status_bar.showMessage(f"Файл {dialog.file_path} открыт", msecs=4000)
        else:
            self.parent.status_bar.showMessage(f"Ошибка открытия файла", msecs=4000)

    def open_manual(self):
        manual = Manual(parent=self)
        self.parent.status_bar.showMessage(f"Открыто руководство", msecs=0)
        manual.show()

    def close_manual(self):
        self.parent.status_bar.showMessage(f"Руководство закрыто", msecs=3000)