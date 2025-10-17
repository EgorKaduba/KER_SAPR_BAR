from PyQt5.QtWidgets import QFileDialog


class FileDialog(QFileDialog):
    def __init__(self, dialog_type: str = "open"):
        QFileDialog.__init__(self)
        self.dialog_type = dialog_type
        self.file_path = None
        path = ""
        if dialog_type == "open":
            path = self.getOpenFileName(caption="KER-SAPR-BAR Open File", directory="./tests", filter="*.json")
        elif dialog_type == "save":
            path = self.getSaveFileName(caption="KER-SAPR-BAR Save File", directory="./tests", filter="*.json")
        if path:
            self.file_path = path[0]