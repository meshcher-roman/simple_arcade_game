import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from game_area import GameArea
from json_reader import load_style_from_json


# ГЛАВНОЕ ОКНО
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flappy Bird")
        self.resize(1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        left_panel_layout = QVBoxLayout()
        left_panel_layout.setContentsMargins(20, 20, 20, 10)
        left_panel_layout.setSpacing(10)

        self.label_score_title = QLabel("SCORE")
        self.label_score_title.setStyleSheet(
            "color: white; font-size: 20px; font-weight: bold;"
        )
        self.label_score_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel_layout.addWidget(self.label_score_title)

        self.label_score_val = QLabel("0")
        self.label_score_val.setStyleSheet(
            "color: #E0C068; font-size: 60px; font-weight: bold;"
        )
        self.label_score_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel_layout.addWidget(self.label_score_val)

        # -- Разделительная линия (для красоты) --
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: white;")
        left_panel_layout.addWidget(line)

        # -- Надпись "BEST" --
        self.label_best_title = QLabel("BEST")
        self.label_best_title.setStyleSheet(
            "color: white; font-size: 20px; font-weight: bold;"
        )
        self.label_best_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel_layout.addWidget(self.label_best_title)

        # -- Цифра Рекорда --
        # Берем начальное значение сразу из game_area
        self.game_area = (
            GameArea()
        )  # Создаем игру чуть ниже, но тут мы пока не можем взять значение...
        self.label_best_val = QLabel("0")
        self.label_best_val.setStyleSheet(
            "color: #E0C068; font-size: 40px; font-weight: bold;"
        )
        self.label_best_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel_layout.addWidget(self.label_best_val)

        left_panel_layout.addStretch(1)

        main_layout.addLayout(left_panel_layout, 1)

        self.game_area = GameArea()
        main_layout.addWidget(self.game_area)
        self.label_best_val.setText(str(self.game_area.high_score))

        right_panel_layout = QVBoxLayout()
        right_panel_layout.setContentsMargins(20, 20, 20, 10)
        self.skin_btn = QPushButton("Change Skin")
        self.skin_btn.setFixedHeight(60)
        self.skin_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        self.skin_btn.setStyleSheet(load_style_from_json("style.json"))
        self.skin_btn.clicked.connect(self.game_area.switch_theme)

        right_panel_layout.addWidget(self.skin_btn)
        right_panel_layout.addStretch(1)
        main_layout.addLayout(right_panel_layout, 1)

        self.game_area.score_updated.connect(self.update_labels)

    def update_labels(self, score, high_score):
        self.label_best_val.setText(str(high_score))
        self.label_score_val.setText(str(score))

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
