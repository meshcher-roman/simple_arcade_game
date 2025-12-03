import json

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtWidgets import QPushButton, QWidget

from bird import Bird
from pipe import Pipe
from theme import Theme

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


class GameArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        # self.setStyleSheet("background-color: #87CEEB;")

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.current_theme = Theme(
            name="Default",
            bg_path="assets/images/background.png",
            bird_path="assets/images/bird.png",
            pipe_path="assets/images/pipe.png",
            # bg_path="assets/images/background_new_year.jpg",
            # bird_path="assets/images/bird_new_year.png",
            # pipe_path="assets/images/pipe_new_year.png",
            text_color_hex="FFFFFF",
        )

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)
        # Создаем птицу
        self.bird = Bird(50, 200)

        self.game_active = True
        self.is_game_over = False

        # Логика добавления труб
        self.pipes = []
        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_pipe)
        self.spawn_timer.start(1500)

        self.restart_btn = QPushButton("Start Game", self)
        self.restart_btn.resize(200, 50)
        self.restart_btn.move(100, 350)

        button_style = self.load_style_from_json("style.json")
        self.restart_btn.setStyleSheet(button_style)
        self.restart_btn.clicked.connect(self.restart_game)
        self.restart_btn.show()
        self.timer.stop()
        self.spawn_timer.stop()
        self.game_active = False

    def load_style_from_json(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Превращаем JSON словарь в строку CSS
            stylesheet = ""
            for selector, properties in data.items():
                stylesheet += f"{selector} {{\n"
                for key, value in properties.items():
                    stylesheet += f"    {key}: {value};\n"
                stylesheet += "}\n"

            return stylesheet
        except Exception as e:
            print(f"Ошибка загрузки стилей: {e}")
            return ""

    def restart_game(self):
        self.game_active = True
        self.is_game_over = False
        self.pipes.clear()
        self.bird.y = 200
        self.bird.velocity = 0

        self.restart_btn.hide()
        self.setFocus()
        self.timer.start(16)
        self.spawn_timer.start(1500)

    def spawn_pipe(self):
        new_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.pipes.append(new_pipe)

    def keyPressEvent(self, event):
        if self.game_active and event.key() == Qt.Key.Key_Space:
            self.bird.jump()

    def update_game(self):
        self.bird.move()

        if self.game_active:
            if self.check_collisions():
                self.game_active = False
                self.spawn_timer.stop()

                self.bird.velocity = 0

            for pipe in self.pipes:
                pipe.move()
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

        if self.is_game_over and not self.timer.isActive():
            # Настраиваем шрифт
            font = QFont("Arial", 40, QFont.Weight.Bold)
            painter.setFont(font)
            painter.setPen(QColor("black"))

            # drawText(x, y, text)
            painter.drawText(40, 200, "GAME OVER")

            # Обводка текста (черная), чтобы читалось лучше (лайфхак)
            painter.setPen(QColor("red"))
            painter.drawText(38, 198, "GAME OVER")

        painter.end()

    def check_collisions(self):
        bird_rect = self.bird.get_rect()

        floor_limit = SCREEN_HEIGHT - self.bird.size
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
