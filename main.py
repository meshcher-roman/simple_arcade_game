import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from bird import Bird
from game_area import GameArea
from pipe import Pipe
from theme import Theme


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
