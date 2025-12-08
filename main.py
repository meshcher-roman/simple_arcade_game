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
from json_reader import (
    load_settings_from_json,
    load_style_from_json,
    save_settings_to_json,
)
from settings_dialog import SettingsDialog
from theme_card import ThemeCard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flappy Bird")

        # 1. ЗАГРУЗКА НАСТРОЕК
        config = load_settings_from_json("settings.json")

        safe_min_width = 1100

        json_min_w = config["window"].get("app_min_width", 1000)
        min_w = max(safe_min_width, json_min_w)
        min_h = config["window"].get("app_min_height", 700)

        self.setMinimumSize(min_w, min_h)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Главный горизонтальный слой
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- СОЗДАНИЕ ИГРЫ ---
        self.game_area = GameArea()
        self.game_area.score_updated.connect(self.update_labels)

        # ==========================================
        # ЛЕВАЯ ПАНЕЛЬ (Статистика + Настройки)
        # ==========================================
        left_panel_widget = QWidget()
        left_panel_widget.setFixedWidth(250)
        left_panel_widget.setStyleSheet("background-color: rgba(0, 0, 0, 150);")

        left_panel_layout = QVBoxLayout(left_panel_widget)
        left_panel_layout.setContentsMargins(20, 50, 20, 20)
        left_panel_layout.setSpacing(10)

        # SCORE
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

        # Линия
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: white;")
        left_panel_layout.addWidget(line)

        # BEST
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

        # --- КНОПКА SETTINGS (Прямо под счетом) ---
        left_panel_layout.addSpacing(20)  # Отступ

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.setFixedHeight(45)  # Чуть повыше
        try:
            self.settings_btn.setStyleSheet(load_style_from_json("style.json"))
        except:
            pass

        # Подключаем сигнал (Только один раз!)
        self.settings_btn.clicked.connect(self.open_settings)

        left_panel_layout.addWidget(self.settings_btn)

        # Пружина внизу (теперь она ПОСЛЕ кнопки, значит кнопка прижмется вверх)
        left_panel_layout.addStretch(1)

        # ==========================================
        # ПРАВАЯ ПАНЕЛЬ (Темы)
        # ==========================================
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

        self.cards_layout.addStretch(1)
        scroll.setWidget(scroll_content)
        self.right_layout.addWidget(scroll)

        # ==========================================
        # СБОРКА ГЛАВНОГО СЛОЯ
        # ==========================================

        # 1. Левая панель
        main_layout.addWidget(left_panel_widget)

        # 2. Пружина слева (Толкает игру к центру)
        main_layout.addStretch(1)

        # 3. ИГРА (По центру)
        main_layout.addWidget(self.game_area)
        # 4. Пружина справа (Толкает игру к центру)
        main_layout.addStretch(1)

        # 5. Правая панель
        main_layout.addWidget(right_panel_widget)

    def on_theme_selected(self, index):
        self.game_area.set_theme(index)
        for i, card in enumerate(self.theme_cards):
            card.set_selected(i == index)
        self.update()

    def update_labels(self, score, high_score):
        self.label_best_val.setText(str(high_score))
        self.label_score_val.setText(str(score))

    def open_settings(self):
        # Создаем и открываем диалог
        dialog = SettingsDialog(self, self.game_area.sounds, self.game_area.config)

        if dialog.exec():
            save_settings_to_json("settings.json", self.game_area.config)

        self.game_area.setFocus()

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
