from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QComboBox, QLabel, QLineEdit, QPushButton)

class AddNodeDialog(QDialog):
    def __init__(self, node_type, node_params, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add {node_type}")
        self.setMinimumWidth(300)
        self.setStyleSheet("""
            QDialog { background-color: #2C2F33; color: white; border-radius: 15px; }
            QLabel { color: white; }
            QLineEdit, QComboBox {
                background-color: #3E4246; border: none; border-radius: 5px;
                padding: 8px; color: white;
            }
            QComboBox QAbstractItemView {
                background-color: #3E4246; color: white; selection-background-color: #5865F2;
            }
            QPushButton {
                background-color: #5865F2; border: none; border-radius: 5px;
                padding: 8px; color: white;
            }
            QPushButton:hover { background-color: #4752C4; }
        """)

        layout = QVBoxLayout(self)

        # Node name input
        self.node_name_input = QLineEdit()
        self.node_name_input.setPlaceholderText("Enter name")
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.node_name_input)

        # Capacity or demand input
        self.capacity_input = QLineEdit()
        self.capacity_input.setPlaceholderText(f"Enter {node_params}")
        layout.addWidget(QLabel(f"{node_params}:"))
        layout.addWidget(self.capacity_input)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.add_btn)
        layout.addLayout(buttons_layout)

    def get_node_data(self):
        """Return the name and capacity/demand."""
        return (self.node_name_input.text().strip(), self.capacity_input.text().strip())
