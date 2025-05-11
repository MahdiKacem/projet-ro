from PyQt5.QtWidgets import  QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class MatrixWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRowCount(0)
        self.setColumnCount(0)
        self.warehouses = []
        self.clients = []
        self.setStyleSheet("""
            QTableWidget {
                background-color: #2C2F33; color: white; gridline-color: #3E4246;
                border-radius: 10px; border: none;
            }
            QTableWidget::item { padding: 5px; border: none; }
            QTableWidget::item:selected { background-color: #5865F2; }
            QHeaderView::section {
                background-color: #23272A; color: white; padding: 5px; border: none;
            }
        """)

    def add_warehouse(self, warehouse_name):
        """Add a warehouse (new row)."""
        if warehouse_name in self.warehouses:
            return
        self.warehouses.append(warehouse_name)
        self.setRowCount(len(self.warehouses))
        self.setVerticalHeaderItem(len(self.warehouses) - 1, QTableWidgetItem(warehouse_name))
        # Fill new row with "∞"
        for j in range(self.columnCount()):
            item = QTableWidgetItem("∞")
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.setItem(len(self.warehouses) - 1, j, item)

    def add_client(self, client_name):
        """Add a client (new column)."""
        if client_name in self.clients:
            return
        self.clients.append(client_name)
        self.setColumnCount(len(self.clients))
        self.setHorizontalHeaderItem(len(self.clients) - 1, QTableWidgetItem(client_name))
        # Fill new column with "∞"
        for i in range(self.rowCount()):
            item = QTableWidgetItem("∞")
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.setItem(i, len(self.clients) - 1, item)

    def add_cost(self, warehouse, client, cost):
        """Add a transportation cost to the matrix."""
        if warehouse not in self.warehouses or client not in self.clients:
            return
        i = self.warehouses.index(warehouse)
        j = self.clients.index(client)
        item = QTableWidgetItem(cost)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.setItem(i, j, item)

    def update_solution(self, solution):
        # Verify table dimensions
        if self.rowCount() != len(self.warehouses) or self.columnCount() != len(self.clients):
            print(
                f"Warning: Table dimensions mismatch. Rows: {self.rowCount()}/{len(self.warehouses)}, Columns: {self.columnCount()}/{len(self.clients)}")
            self.setRowCount(len(self.warehouses))
            self.setColumnCount(len(self.clients))

        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                try:
                    w = self.warehouses[i]
                    c = self.clients[j]
                    qty = solution.get((w, c), 0)
                    if qty > 0:
                        qty_text = f"{int(qty)}" if qty.is_integer() else f"{qty:.2f}"
                        item = QTableWidgetItem(qty_text)
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                        item.setBackground(QColor("#CE7B91"))
                        self.setItem(i, j, item)
                    else:
                        current_item = self.item(i, j)
                        if current_item and current_item.text() and current_item.text() != "∞":
                            try:
                                # Verify the text is a valid number (original cost)
                                float(current_item.text())
                                item = QTableWidgetItem(current_item.text())
                                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                                self.setItem(i, j, item)
                            except ValueError:
                                # If text is invalid, set to "∞"
                                item = QTableWidgetItem("∞")
                                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                                self.setItem(i, j, item)
                        else:
                            # Set to "∞" if cell is empty or invalid
                            item = QTableWidgetItem("∞")
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                            self.setItem(i, j, item)
                except Exception as e:
                    print(f"Error in MatrixWidget.update_solution at cell ({i}, {j}): {e}")

    def get_cost_matrix(self):
        """Return the cost matrix as a dictionary."""
        cost = {}
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                weight = self.item(i, j).text()
                if weight != "∞":
                    cost[(self.warehouses[i], self.clients[j])] = int(weight)
        return cost