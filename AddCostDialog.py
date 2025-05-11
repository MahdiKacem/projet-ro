from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QComboBox, QLabel, QLineEdit, QPushButton)

class AddCostDialog(QDialog):
    def __init__(self, parent=None, warehouses=None, clients=None):
        super().__init__(parent)
        self.setWindowTitle("Add Transportation Cost")
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog { background-color: #2C2F33; color: white; border-radius: 15px; }
            QLabel { color: white; }
            QComboBox {
                background-color: #3E4246; border: none; border-radius: 5px;
                padding: 8px; color: white;
            }
            QComboBox QAbstractItemView {
                background-color: #3E4246; color: white; selection-background-color: #5865F2;
            }
            QLineEdit {
                background-color: #3E4246; border: none; border-radius: 5px;
                padding: 8px; color: white;
            }
            QPushButton {
                background-color: #5865F2; border: none; border-radius: 5px;
                padding: 8px; color: white;
            }
            QPushButton:hover { background-color: #4752C4; }
        """)

        layout = QVBoxLayout(self)

        # Warehouse selection
        self.warehouse_combo = QComboBox()
        self.warehouse_combo.addItems(warehouses if warehouses else [])
        layout.addWidget(QLabel("Warehouse:"))
        layout.addWidget(self.warehouse_combo)

        # Client selection
        self.client_combo = QComboBox()
        self.client_combo.addItems(clients if clients else [])
        layout.addWidget(QLabel("Client:"))
        layout.addWidget(self.client_combo)

        # Cost input
        self.cost_input = QLineEdit()
        self.cost_input.setPlaceholderText("Enter transportation cost")
        layout.addWidget(QLabel("Cost:"))
        layout.addWidget(self.cost_input)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.add_btn)
        layout.addLayout(buttons_layout)

    def get_cost_data(self):
        """Return selected warehouse, client, and cost."""
        return (self.warehouse_combo.currentText(), self.client_combo.currentText(),
                self.cost_input.text().strip())