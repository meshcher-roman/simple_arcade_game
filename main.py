import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

# Константы
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


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


# ИГРОВАЯ ОБЛАСТЬ
class GameArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setStyleSheet("background-color: #87CEEB;")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)
        # Создаем птицу
        self.bird = Bird(50, 200)

    def update_game(self):
        self.bird.move()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.bird.draw(painter)
        painter.end()


# ГЛАВНОЕ ОКНО
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flappy Bird")
        self.resize(600, 800)
        self.setStyleSheet("background-color: #333;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        self.game_area = GameArea()
        layout.addWidget(self.game_area, alignment=Qt.AlignmentFlag.AlignCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
