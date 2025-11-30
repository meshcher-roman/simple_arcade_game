from PyQt6.QtCore import QRectF, Qt
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

        if self.y < 0:
            self.y = 0  # Не пускаем выше края
            self.velocity = (
                0  # Гасим инерцию подлета, чтобы она сразу могла начать падать
            )

    def draw(self, painter, bird_pixmap):
        painter.drawPixmap(int(self.x), int(self.y), self.size, self.size, bird_pixmap)

    def jump(self):
        self.velocity = -7

    def get_rect(self):
        return QRectF(self.x, self.y, self.size * 0.8, self.size * 0.7)
