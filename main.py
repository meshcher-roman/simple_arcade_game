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
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from game_area import GameArea
from json_reader import load_style_from_json
from theme_card import ThemeCard


# ГЛАВНОЕ ОКНО
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flappy Bird")

        self.setMinimumSize(1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- СОЗДАНИЕ ИГРЫ ---
        self.game_area = GameArea()
        self.game_area.score_updated.connect(self.update_labels)

        # --- ЛЕВАЯ ПАНЕЛЬ ---
        left_panel_widget = QWidget()
        left_panel_widget.setFixedWidth(250)  # Чуть шире, чтобы текст влезал
        left_panel_widget.setStyleSheet("background-color: rgba(0, 0, 0, 150);")

        left_panel_layout = QVBoxLayout(left_panel_widget)
        left_panel_layout.setContentsMargins(20, 50, 20, 20)
        left_panel_layout.setSpacing(15)

        self.label_score_title = QLabel("SCORE")
        self.label_score_title.setStyleSheet(
            "color: white; font-size: 24px; font-weight: bold; background: transparent;"
        )
        self.label_score_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel_layout.addWidget(self.label_score_title)

        self.label_score_val = QLabel("0")
        self.label_score_val.setStyleSheet(
            "color: #E0C068; font-size: 60px; font-weight: bold; background: transparent;"
        )
        self.label_score_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel_layout.addWidget(self.label_score_val)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: white;")
        left_panel_layout.addWidget(line)

        self.label_best_title = QLabel("BEST")
        self.label_best_title.setStyleSheet(
            "color: white; font-size: 24px; font-weight: bold; background: transparent;"
        )
        self.label_best_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel_layout.addWidget(self.label_best_title)

        self.label_best_val = QLabel(str(self.game_area.high_score))
        self.label_best_val.setStyleSheet(
            "color: #E0C068; font-size: 40px; font-weight: bold; background: transparent;"
        )
        self.label_best_val.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_panel_layout.addWidget(self.label_best_val)

        left_panel_layout.addStretch(1)

        # --- ПРАВАЯ ПАНЕЛЬ ---
        right_panel_widget = QWidget()
        right_panel_widget.setFixedWidth(250)
        right_panel_widget.setStyleSheet("background-color: rgba(0, 0, 0, 150);")

        self.right_layout = QVBoxLayout(right_panel_widget)
        self.right_layout.setContentsMargins(20, 20, 20, 20)

        title_lbl = QLabel("THEMES")
        title_lbl.setStyleSheet(
            "color: white; font-weight: bold; font-size: 20px; background: transparent;"
        )
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_layout.addWidget(title_lbl)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.cards_layout = QVBoxLayout(scroll_content)
        self.cards_layout.setSpacing(20)

        self.theme_cards = []
        for i, theme in enumerate(self.game_area.themes):
            is_active = i == self.game_area.current_theme_index
            card = ThemeCard(theme, i, is_active)
            card.clicked.connect(self.on_theme_selected)
            self.cards_layout.addWidget(card)
            self.theme_cards.append(card)

        self.cards_layout.addStretch(1)  # Чтобы карточки были прижаты к верху
        scroll.setWidget(scroll_content)
        self.right_layout.addWidget(scroll)

        # --- СБОРКА ГЛАВНОГО СЛОЯ ---

        main_layout.addWidget(left_panel_widget)

        main_layout.addStretch(1)

        main_layout.addWidget(self.game_area, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addStretch(1)

        main_layout.addWidget(right_panel_widget)

    def on_theme_selected(self, index):
        self.game_area.set_theme(index)
        for i, card in enumerate(self.theme_cards):
            card.set_selected(i == index)
        self.update()

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
