import random

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class Pipe:
    def __init__(self, x, screen_height):
        self.screen_height = screen_height
        self.x = x

        # Параметры труб
        self.width = 60
        self.speed = 3
        self.gap_size = 150
        self.color = QColor("228B22")

        # Логика вычисления высоты пролета
        min_y = 50
        max_y = screen_height - min_y - self.gap_size
        self.gap_y = random.randint(min_y, max_y)

    def move(self):
        self.x -= self.speed

    def draw(self, painter):
        painter.setBrush(self.color)
        painter.setPen(Qt.PenStyle.NoPen)

        # Отрисовка верхней трубы
        painter.drawRect(int(self.x), 0, self.width, self.gap_y)

        # Отрисовка нижней трубы
        bottom_y = self.gap_y + self.gap_size
        bottom_height = self.screen_height - bottom_y

        painter.drawRect(int(self.x), bottom_y, self.width, bottom_height)
