import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from game_area import GameArea
from json_to_str_reader import load_style_from_json


# ГЛАВНОЕ ОКНО
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flappy Bird")
        self.resize(1000, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.addStretch(1)

        self.game_area = GameArea()
        main_layout.addWidget(self.game_area)

        right_panel_layout = QVBoxLayout()
        right_panel_layout.setContentsMargins(20, 0, 20, 0)
        self.skin_btn = QPushButton("Change Skin")
        self.skin_btn.setFixedSize(150, 50)

        self.skin_btn.setStyleSheet(load_style_from_json("style.json"))
        self.skin_btn.clicked.connect(self.game_area.switch_theme)

        right_panel_layout.addWidget(self.skin_btn)
        right_panel_layout.addStretch(1)
        main_layout.addLayout(right_panel_layout, 1)

    def paintEvent(self, event):
        painter = QPainter(self)
        if hasattr(self, "game_area") and hasattr(self.game_area, "current_theme"):
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
