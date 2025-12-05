import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from game_area import GameArea


# ГЛАВНОЕ ОКНО
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flappy Bird")
        self.resize(800, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        self.game_area = GameArea()
        layout.addWidget(self.game_area, alignment=Qt.AlignmentFlag.AlignCenter)

    def paintEvent(self, event):
        painter = QPainter(self)
        blurred_pixmap = self.game_area.current_theme.blurred_bg
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.drawPixmap(self.rect(), blurred_pixmap)

        overlay_color = QColor(0, 0, 0, 100)
        painter.fillRect(self.rect(), overlay_color)
        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
