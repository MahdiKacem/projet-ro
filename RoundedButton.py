from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt

class RoundedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(36)
        self.setCursor(Qt.PointingHandCursor)
