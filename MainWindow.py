from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QWidget, QSizePolicy)
from PyQt5.QtCore import Qt
from gurobipy import Model, GRB
from RoundedButton import RoundedButton

from AddCostDialog import AddCostDialog
from AddNodeDialog import AddNodeDialog
from GraphVisualizationWidget import GraphVisualizationWidget
from MatrixWidget import MatrixWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transportation Problem Solver")
        self.resize(1200, 700)
        self.warehouses = {}
        self.clients = {}

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_panel.setMinimumWidth(550)
        left_panel_layout = QVBoxLayout(left_panel)
        left_panel_layout.setContentsMargins(15, 15, 15, 15)
        left_panel_layout.setSpacing(15)

        buttons_layout = QHBoxLayout()
        self.add_node_btn = RoundedButton("Add Warehouse")
        self.add_node_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.add_node_btn.clicked.connect(self.show_add_warehouse_dialog)
        buttons_layout.addWidget(self.add_node_btn, stretch=1)

        self.add_node_btn = RoundedButton("Add Client")
        self.add_node_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.add_node_btn.clicked.connect(self.show_add_client_dialog)
        buttons_layout.addWidget(self.add_node_btn, stretch=1)

        self.add_cost_btn = RoundedButton("Add Cost")
        self.add_node_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.add_cost_btn.clicked.connect(self.show_add_cost_dialog)
        buttons_layout.addWidget(self.add_cost_btn, stretch=1)

        self.solve_btn = RoundedButton("Solve")
        self.add_node_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.solve_btn.clicked.connect(self.solve_transportation_problem)
        buttons_layout.addWidget(self.solve_btn, stretch=1)

        buttons_layout.addStretch()
        left_panel_layout.addLayout(buttons_layout)

        matrix_container = QFrame()
        matrix_container.setObjectName("matrixContainer")
        matrix_container_layout = QVBoxLayout(matrix_container)
        matrix_container_layout.setContentsMargins(15, 15, 15, 15)

        matrix_label = QLabel("Cost Matrix")
        matrix_label.setAlignment(Qt.AlignCenter)
        matrix_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        matrix_container_layout.addWidget(matrix_label)

        self.matrix_widget = MatrixWidget()
        matrix_container_layout.addWidget(self.matrix_widget)

        self.solution_label = QLabel("")
        self.solution_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
        matrix_container_layout.addWidget(self.solution_label)

        left_panel_layout.addWidget(matrix_container)

        right_panel = QFrame()
        right_panel.setObjectName("rightPanel")
        right_panel_layout = QVBoxLayout(right_panel)
        right_panel_layout.setContentsMargins(15, 15, 15, 15)

        result_container = QFrame()
        result_container.setObjectName("resultContainer")
        result_container_layout = QVBoxLayout(result_container)
        result_container_layout.setContentsMargins(15, 15, 15, 15)

        result_label = QLabel("Result")
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        result_container_layout.addWidget(result_label)

        self.solution_label = QLabel("")
        self.solution_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")
        result_container_layout.addWidget(self.solution_label)
        left_panel_layout.addWidget(result_container)


        self.graph_view = GraphVisualizationWidget()
        right_panel_layout.addWidget(self.graph_view)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2C2F33; color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QFrame#leftPanel, QFrame#rightPanel {
                background-color: #23272A; border-radius: 15px;
            }
            QFrame#matrixContainer {
                background-color: #2C2F33; border-radius: 15px; border: 1px solid #3E4246;
            }
            QPushButton {
                background-color: #5865F2; border: none; border-radius: 5px;
                padding: 8px; color: white;
            }
            QPushButton:hover { background-color: #4752C4; }
            QFrame#resultContainer {
                background-color: #2C2F33; 
                border-radius: 15px; 
                border: 1px solid #3E4246;
            }

        """)

    def add_node(self, node_type, node_name, capacity, index):
        if node_name in self.warehouses or node_name in self.clients:
            return
        try:
            capacity = int(capacity)
            if capacity < 0:
                raise ValueError("Capacity must be non-negative")
        except ValueError:
            self.solution_label.setText("Error: Invalid capacity/demand")
            return
        if node_type == "Warehouse":
            self.warehouses[node_name] = capacity
            self.matrix_widget.add_warehouse(node_name)
        else:
            self.clients[node_name] = capacity
            self.matrix_widget.add_client(node_name)
        self.graph_view.add_node(node_name, node_type, index, capacity)

    def add_cost(self, warehouse, client, cost):
        try:
            cost = int(cost)
            if cost < 0:
                raise ValueError("Cost must be non-negative")
        except ValueError:
            self.solution_label.setText("Error: Invalid cost")
            return
        self.matrix_widget.add_cost(warehouse, client, str(cost))
        self.graph_view.add_edge(warehouse, client, cost)

    def show_add_warehouse_dialog(self):
        dialog = AddNodeDialog("Warehouse", "Capacity", self)
        if dialog.exec_():
            node_name, capacity = dialog.get_node_data()
            if node_name and capacity:
                index = len(self.warehouses)
                self.add_node("Warehouse", node_name, capacity, index)
                self.graph_view.add_node(node_name, "Warehouse", index, capacity)
                print(f"Added warehouse: {node_name}, Capacity: {capacity}")

    def show_add_client_dialog(self):
        dialog = AddNodeDialog("Client", "Demand", self)
        if dialog.exec_():
            node_name, demand = dialog.get_node_data()
            if node_name and demand:
                index = len(self.clients)
                self.add_node("Client", node_name, demand, index)
                self.graph_view.add_node(node_name, "Client", index, demand)
                print(f"Added client: {node_name}, Demand: {demand}")

    def show_add_cost_dialog(self):
        dialog = AddCostDialog(self, self.warehouses.keys(), self.clients.keys())
        if dialog.exec_():
            warehouse, client, cost = dialog.get_cost_data()
            if warehouse and client and cost:
                self.add_cost(warehouse, client, cost)
                print(f"Added cost: {warehouse} -> {client}, Cost: {cost}")

    def solve_transportation_problem(self):
        cost = self.matrix_widget.get_cost_matrix()

        model = Model("Transport_Optimization")
        x = model.addVars(self.warehouses.keys(), 
                          self.clients.keys(),
                          vtype=GRB.INTEGER, 
                          lb=0, 
                          name="x")
        model.setObjective(
            sum(cost.get((w, c), 0) * x[w, c] for w in self.warehouses for c in self.clients),
            GRB.MINIMIZE)

        for w in self.warehouses:
            model.addConstr(sum(x[w, c] for c in self.clients) <= self.warehouses[w], f"Supply_{w}")

        for c in self.clients:
            model.addConstr(sum(x[w, c] for w in self.warehouses) >= self.clients[c], f"Demand_{c}")

        model.optimize()

        if model.status == GRB.OPTIMAL:
            solution = {(w, c): x[w, c].x for w in self.warehouses for c in self.clients if x[w, c].x > 0}
            message = [f"Optimal Solution Found: Total Cost = {model.objVal:.2f}"]
            for (w, c), qty in solution.items():
                message.append(f"Ship {qty} units from {w} to {c} (cost per unit: {cost.get((w, c), 0)})")
            self.solution_label.setText("\n".join(message))
            self.matrix_widget.update_solution(solution)
            self.graph_view.highlight_solution(solution)
        elif model.status == GRB.INFEASIBLE:
            self.solution_label.setText("Model is infeasible. Check inputs.")
        else:
            self.solution_label.setText(f"Solution not optimal. Status: {model.status}")