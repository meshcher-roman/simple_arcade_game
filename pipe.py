import random

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor, QTransform


class Pipe:
    def __init__(self, x, screen_height):
        self.screen_height = screen_height
        self.x = x
        # Параметры труб
        self.width = 60
        self.speed = 3
        self.gap_size = 150
        self.color = QColor("228B22")
        self.passed = False

        # Логика вычисления высоты пролета
        min_y = 50
        max_y = screen_height - min_y - self.gap_size
        self.gap_y = random.randint(min_y, max_y)

    def move(self):
        self.x -= self.speed

    def draw(self, painter, pipe_pixmap):
        img_w = pipe_pixmap.width()
        img_h = pipe_pixmap.height()
        # Отрисовка верхней трубы
        flipped_pixmap = pipe_pixmap.transformed(QTransform().scale(1, -1))
        top_height = self.gap_y
        source_h = min(img_h, int(top_height))
        source_y = img_h - source_h
        painter.drawPixmap(
            int(self.x),
            0,
            self.width,
            int(top_height),
            flipped_pixmap,
            0,
            source_y,
            img_w,
            source_h,
        )

        # Отрисовка нижней трубы
        bottom_y = self.gap_y + self.gap_size
        bottom_height = self.screen_height - bottom_y

        source_h = min(img_h, int(bottom_height))

        painter.drawPixmap(
            int(self.x),
            bottom_y,
            self.width,
            bottom_height,
            pipe_pixmap,
            0,
            0,
            img_w,
            source_h,
        )

    def get_rects(self):
        top_rect = QRectF(self.x, 0, self.width, self.gap_y)

        bottom_y = self.gap_y + self.gap_size
        bottom_height = self.screen_height - bottom_y
        bottom_rect = QRectF(self.x, bottom_y, self.width, bottom_height)

        return top_rect, bottom_rect
