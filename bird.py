from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class Bird:
    def __init__(self, x, y, size=30, color="#FFD700"):
        self.x = x
        self.y = y
        self.size = size
        self.color = QColor(color)

        self.velocity = 0
        self.gravity = 0.5

    def move(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self, painter):
        painter.setBrush(self.color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(self.x), int(self.y), self.size, self.size)
