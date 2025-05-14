from math import atan2, cos, radians, sin

from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene,
                             QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem, QGraphicsRectItem)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QPointF

class GraphVisualizationWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.scene = QGraphicsScene(self)
        self.scene.setBackgroundBrush(QColor("#1E2124"))
        self.setScene(self.scene)
        self.nodes = {}
        self.edges = []
        self.edgeItems = {}

    def add_node(self, node_name, node_type, index, value):
        """Add a node to the graph (warehouse or client) with an optional supply/demand value."""
        if node_name in self.nodes: #or len(self.nodes) >= 20:
            # Prevent adding more than 10 nodes or duplicate names
            return

        # Define shape and color based on node type
        if node_type == "Warehouse":
            shape = QGraphicsRectItem(-20, -20, 40, 40)  # Rectangle for warehouse
            color = "#0081A7"
        else:
            shape = QGraphicsEllipseItem(-20, -20, 40, 40)  # Circle for client
            color = "#F07167"

        # Set shape properties
        shape.setBrush(QBrush(QColor(color)))
        shape.setPen(QPen(Qt.NoPen))
        shape.setZValue(1)
        self.scene.addItem(shape)

        # Add node name as text inside the shape
        text = QGraphicsTextItem(node_name)
        text.setDefaultTextColor(QColor("#FFFFFC"))
        text.setFont(QFont("Segoe UI", 10, QFont.Bold))
        text.setParentItem(shape)  # Attach text to the shape
        text.setPos(-text.boundingRect().width() / 2, -text.boundingRect().height() / 2)

        # Position nodes in a bipartite layout
        x = -200 if node_type == "Warehouse" else 200
        y = index * 100 - 200
        shape.setPos(x, y)

        # Add supply/demand value as a separate text item BELOW the node
        value_text = QGraphicsTextItem(f"{value}")
        value_text.setDefaultTextColor(QColor("#D1D1D1"))
        value_text.setFont(QFont("Segoe UI", 9))
        # Attach the value text to the shape to move together
        value_text.setParentItem(shape)  
        # Position the value text slightly below the shape
        value_text.setPos(-value_text.boundingRect().width() / 2, 25)  
        self.scene.addItem(value_text)

        # Store the node and its associated text items
        self.nodes[node_name] = shape


    def add_edge(self, warehouse, client, cost):
        """Add an edge from warehouse to client."""
        if warehouse not in self.nodes or client not in self.nodes:
            return
        pos1 = self.nodes[warehouse].scenePos()
        pos2 = self.nodes[client].scenePos()
        edge_key = (warehouse, client)
        items = self._draw_edge(pos1, pos2, cost)
        self.edgeItems[edge_key] = items
        self.edges.append(edge_key)

    def _draw_edge(self, start, end, weight):
        """Draw a directed edge with weight label."""
        items_created = []
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        length = (dx**2 + dy**2) ** 0.5
        shrink = 20
        ratio = (length - shrink) / length if length != 0 else 1
        adjusted_end = QPointF(start.x() + dx * ratio, start.y() + dy * ratio)

        line = QGraphicsLineItem(start.x(), start.y(), adjusted_end.x(), adjusted_end.y())
        pen = QPen(QColor("#FFFFFF"), 2)
        line.setPen(pen)
        self.scene.addItem(line)
        items_created.append(line)

        mid = QPointF((start.x() + adjusted_end.x()) / 2, (start.y() + adjusted_end.y()) / 2)
        text = QGraphicsTextItem(str(weight))
        text.setDefaultTextColor(Qt.white)
        text.setFont(QFont("Segoe UI", 10))
        x_offset = 50 if dx > 0 else -50  # Adjust to the right if moving right
        y_offset = -5 if dy > 0 else 5  # Adjust downward if moving upward
        text.setPos(mid.x() + x_offset, mid.y() + y_offset)
        self.scene.addItem(text)
        items_created.append(text)

        arrow_items = self._draw_arrowhead(start, adjusted_end)
        items_created.extend(arrow_items)
        return items_created

    def _draw_arrowhead(self, start, end):
        """Draw an arrowhead."""
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        angle = atan2(dy, dx)
        arrow_size = 10
        arrow_base_x = end.x()
        arrow_base_y = end.y()
        p1 = QPointF(
            arrow_base_x - arrow_size * cos(angle - radians(30)),
            arrow_base_y - arrow_size * sin(angle - radians(30))
        )
        p2 = QPointF(
            arrow_base_x - arrow_size * cos(angle + radians(30)),
            arrow_base_y - arrow_size * sin(angle + radians(30))
        )
        arrow_line1 = QGraphicsLineItem(end.x(), end.y(), p1.x(), p1.y())
        arrow_line2 = QGraphicsLineItem(end.x(), end.y(), p2.x(), p2.y())
        pen = QPen(QColor("#FFFFFF"), 2)
        arrow_line1.setPen(pen)
        arrow_line2.setPen(pen)
        self.scene.addItem(arrow_line1)
        self.scene.addItem(arrow_line2)
        return [arrow_line1, arrow_line2]

    def highlight_solution(self, solution):
        # Store original costs to restore if needed
        original_texts = {edge: items[1].toPlainText() for edge, items in self.edgeItems.items() if
                          len(items) > 1 and isinstance(items[1], QGraphicsTextItem)}

        for edge in self.edgeItems:
            try:
                items = self.edgeItems[edge]
                w, c = edge
                qty = solution.get(edge, 0)
                color = "#CE7B91" if qty > 0 else "#FFFFFF"
                for item in items:
                    if isinstance(item, QGraphicsLineItem):
                        pen = QPen(QColor(color), 2)
                        item.setPen(pen)
                    elif isinstance(item, QGraphicsTextItem) and qty > 0:
                        item.setDefaultTextColor(QColor(color))
                        qty_text = f"{int(qty)}" if qty.is_integer() else f"{qty:.2f}"
                        # Show both cost and quantity
                        original_cost = original_texts.get(edge, "0")
                        item.setPlainText(f"{original_cost} ({qty_text})")
                    elif isinstance(item, QGraphicsTextItem):
                        # Restore original cost if qty is 0
                        item.setDefaultTextColor(QColor("#FFFFFF"))
                        item.setPlainText(original_texts.get(edge, "0"))
            except Exception as e:
                print(f"Error in GraphVisualizationWidget.highlight_solution for edge {edge}: {e}")

    def resizeEvent(self, event):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(event)