import math
import sys

from PyQt6.QtCore import QSettings, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtWidgets import QPushButton, QWidget

from bird import Bird
from json_reader import (
    load_settings_from_json,
    load_style_from_json,
    load_themes_from_json,
)
from pipe import Pipe


class GameArea(QWidget):
    score_updated = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

        # 1. ЗАГРУЖАЕМ НАСТРОЙКИ
        self.config = load_settings_from_json("settings.json")

        # Достаем параметры окна для удобства
        self.SCREEN_WIDTH = self.config["window"]["screen_width"]
        self.SCREEN_HEIGHT = self.config["window"]["screen_height"]

        self.hover_frame = 0
        self.ready_to_start = False
        self.settings = QSettings("MyApp", "FlappyBird")
        self.high_score = int(self.settings.value("high_score", 0))
        self.score = 0

        # Используем загруженные размеры
        self.setFixedSize(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.themes = load_themes_from_json("themes.json")
        self.current_theme_index = 0
        if self.themes:
            self.current_theme = self.themes[self.current_theme_index]
        else:
            print("Критическая ошибка: Темы не загружены!")
            sys.exit()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        # FPS можно тоже брать из конфига (1000 / 60 = 16ms)
        self.timer.start(1000 // self.config["gameplay"]["fps"])

        # Создаем птицу с параметрами из конфига
        b_conf = self.config["bird"]
        self.bird = Bird(
            x=b_conf["start_x"],
            y=b_conf["start_y"],
            size=b_conf["size"],
            gravity=b_conf["gravity"],
            jump_velocity=b_conf["jump_velocity"],
            rotation_multiplier=b_conf["rotation_multiplier"],
        )

        self.game_active = True
        self.is_game_over = False

        self.pipes = []
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_pipe)
        # Интервал спавна из конфига
        self.spawn_timer.start(self.config["gameplay"]["spawn_interval"])

        self.restart_btn = QPushButton("Start Game", self)
        self.restart_btn.resize(200, 50)
        # Центрируем кнопку (примерно)
        self.restart_btn.move(self.SCREEN_WIDTH // 2 - 100, 350)

        button_style = load_style_from_json("style.json")
        self.restart_btn.setStyleSheet(button_style)
        self.restart_btn.clicked.connect(self.restart_game)
        self.restart_btn.show()
        self.timer.stop()
        self.spawn_timer.stop()
        self.game_active = False
        self.reset_game()

    def set_theme(self, index):
        if 0 <= index < len(self.themes):
            self.current_theme_index = index
            self.current_theme = self.themes[index]
            self.update()  # Перерисовать игру

            # Обновить главное окно (фон)
            if self.window():
                self.window().update()

    def reset_game(self):
        self.game_active = False
        self.ready_to_start = True
        self.is_game_over = False

        self.pipes.clear()
        # Сброс позиции из конфига
        self.bird.y = self.config["bird"]["start_y"]
        self.bird.velocity = 0
        self.score = 0
        self.score_updated.emit(self.score, self.high_score)
        self.restart_btn.hide()
        self.setFocus()
        self.timer.start(1000 // self.config["gameplay"]["fps"])
        self.spawn_timer.stop()

    def restart_game(self):
        self.reset_game()

    def spawn_pipe(self):
        # Передаем настройки труб в новую трубу
        new_pipe = Pipe(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.config["pipe"])
        self.pipes.append(new_pipe)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            if self.ready_to_start:
                self.ready_to_start = False
                self.game_active = True
                self.spawn_timer.start(self.config["gameplay"]["spawn_interval"])
                self.bird.jump()

            elif self.game_active:
                self.bird.jump()

    # ... update_game почти без изменений, только замени 200 на self.config["bird"]["start_y"] ...
    def update_game(self):
        if self.ready_to_start:
            self.hover_frame += 0.1
            self.bird.y = (
                self.config["bird"]["start_y"] + math.sin(self.hover_frame) * 10
            )
            self.update()
            return

        self.bird.move()

        if self.game_active:
            if self.check_collisions():
                self.game_active = False
                self.spawn_timer.stop()

                self.bird.velocity = 0

            for pipe in self.pipes:
                pipe.move()
                if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                    self.score += 1
                    pipe.passed = True

                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.settings.setValue("high_score", self.high_score)
                    self.score_updated.emit(self.score, self.high_score)
            self.pipes = [p for p in self.pipes if p.x + p.width > 0]

        else:
            self.check_collisions()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.drawPixmap(
            0, 0, self.width(), self.height(), self.current_theme.background_img
        )

        pipe_texture = self.current_theme.pipe_img
        for pipe in self.pipes:
            pipe.draw(painter, pipe_texture)
        bird_texture = self.current_theme.bird_img
        self.bird.draw(painter, bird_texture)
        if self.ready_to_start:
            font = QFont("Arial", 20, QFont.Weight.Bold)
            painter.setFont(font)

            text = "Press SPACE to Start"

            # Тень
            painter.setPen(QColor("black"))
            painter.drawText(
                2, 302, self.width(), 50, Qt.AlignmentFlag.AlignCenter, text
            )

            # Текст
            painter.setPen(QColor("white"))
            painter.drawText(
                0, 300, self.width(), 50, Qt.AlignmentFlag.AlignCenter, text
            )
        if self.is_game_over and not self.timer.isActive():
            # Настраиваем шрифт
            font = QFont("Arial", 40, QFont.Weight.Bold)
            painter.setFont(font)
            painter.setPen(QColor("black"))

            painter.drawText(40, 200, "GAME OVER")

            painter.setPen(QColor("red"))
            painter.drawText(38, 198, "GAME OVER")

        painter.end()

    def check_collisions(self):
        bird_rect = self.bird.get_rect()
        # Используем динамическую высоту экрана
        floor_limit = self.SCREEN_HEIGHT - self.bird.size

        if self.bird.y >= floor_limit:
            self.bird.y = floor_limit
            self.timer.stop()
            self.spawn_timer.stop()
            self.game_active = False
            self.is_game_over = True
            self.restart_btn.setText("Restart")
            self.restart_btn.show()
            return False

        if self.game_active:
            for pipe in self.pipes:
                top_rect, bottom_rect = pipe.get_rects()
                if bird_rect.intersects(top_rect) or bird_rect.intersects(bottom_rect):
                    return True
        return False

    def switch_theme(self):
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        self.current_theme = self.themes[self.current_theme_index]
        self.update()

        if self.window():
            self.window().update()
