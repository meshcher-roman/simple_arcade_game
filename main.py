import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from bird import Bird
from pipe import Pipe

# Константы
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


# ИГРОВАЯ ОБЛАСТЬ
class GameArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setStyleSheet("background-color: #87CEEB;")

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)
        # Создаем птицу
        self.bird = Bird(50, 200)

        # Логика добавления труб
        self.pipes = []
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_pipe)
        self.spawn_timer.start(1500)

    def spawn_pipe(self):
        new_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.pipes.append(new_pipe)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.bird.jump()

    def update_game(self):
        self.bird.move()
        for pipe in self.pipes:
            pipe.move()
            self.pipes = [p for p in self.pipes if p.x + p.width > 0]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        for pipe in self.pipes:
            pipe.draw(painter)
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
