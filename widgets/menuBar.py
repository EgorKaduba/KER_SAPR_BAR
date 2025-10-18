import json

from PyQt5.QtWidgets import QMenuBar, QMenu, QAction
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt

from widgets.fileDialog import FileDialog
from widgets.manual import Manual
from widgets.validators import DataValidator

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        QMenuBar.__init__(self, parent)
        self.parent = parent
        self.setup_menu_bar()

    def setup_menu_bar(self):
        file_menu = QMenu("&Файл", self)

        open_action = QAction(QIcon("images/icons/open_icon.png"), "Открыть", file_menu)
        open_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_O))
        open_action.triggered.connect(self.open_file)  # noqa
        save_action = QAction(QIcon("images/icons/save_icon.png"), "Сохранить", file_menu)
        save_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_S))
        save_action.triggered.connect(self.save_file)  # noqa
        exit_action = QAction(QIcon("images/icons/exit_icon.png"), "Выход", file_menu)
        exit_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_C))
        exit_action.triggered.connect(self.parent.close)  # noqa

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        reference_menu = QMenu("Справка", self)

        manual_action = QAction(QIcon("images/icons/manual_icon.png"), "Руководство", reference_menu)
        manual_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_I))
        manual_action.triggered.connect(self.open_manual)  # noqa

        reference_menu.addAction(manual_action)

        self.addMenu(file_menu)
        self.addMenu(reference_menu)

    def save_file(self):
        if not self.parent.file_path:
            dialog = FileDialog(dialog_type="save")
            if dialog.file_path:
                info = self.parent.preprocessor.get_all_info()
                validation_errors = DataValidator.validate_all_data(info)
                if validation_errors:
                    error_msg = "Ошибки валидации:\n" + "\n".join(validation_errors)
                    self.parent.status_bar.showMessage(f"Ошибки в данных: {error_msg}", msecs=8000)
                    return

                try:
                    with open(dialog.file_path, "w", encoding='utf-8') as file:
                        json_data = json.dumps(info, ensure_ascii=False, indent=2)
                        file.write(json_data)
                    self.parent.status_bar.showMessage(f"Файл {dialog.file_path} сохранён", msecs=4000)
                    self.parent.file_path = dialog.file_path
                except Exception as error_msg:
                    self.parent.status_bar.showMessage(f"Ошибка сохранения: {error_msg}", msecs=4000)
            else:
                self.parent.status_bar.showMessage("Ошибка сохранения файла", msecs=4000)

    def open_file(self):
        dialog = FileDialog(dialog_type="open")
        if dialog.file_path:
            try:
                with open(dialog.file_path, "r", encoding='utf-8') as file:
                    json_data = file.read()
                    info_dict = json.loads(json_data)

                validation_errors = DataValidator.validate_all_data(info_dict)
                if validation_errors:
                    error_msg = "Ошибки в файле:\n" + "\n".join(validation_errors[:5])
                    self.parent.status_bar.showMessage(f"Ошибки валидации: {error_msg}", msecs=8000)
                    return

                if info_dict:
                    self.parent.preprocessor.filling_from_file(info_dict)
                    self.parent.file_path = dialog.file_path
                    self.parent.status_bar.showMessage(f"Файл {dialog.file_path} открыт", msecs=4000)

            except Exception as e:
                self.parent.status_bar.showMessage(f"Ошибка чтения файла: {str(e)}", msecs=4000)
        else:
            self.parent.status_bar.showMessage("Ошибка открытия файла", msecs=4000)

    def open_manual(self):
        manual = Manual(parent=self)
        self.parent.status_bar.showMessage(f"Открыто руководство", msecs=0)
        manual.show()

    def close_manual(self):
        self.parent.status_bar.showMessage(f"Руководство закрыто", msecs=3000)