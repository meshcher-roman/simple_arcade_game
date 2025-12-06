from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QPixmap


class Theme:
    def __init__(self, name, bg_path, bird_path, pipe_path, text_color_hex):
        self.name = name

        self.background_img = QPixmap(bg_path)
        self.bird_img = QPixmap(bird_path)
        self.pipe_img = QPixmap(pipe_path)

        self.text_color = QColor(text_color_hex)

        small_w = self.background_img.width() // 10
        small_h = self.background_img.height() // 10

        self.blurred_bg = self.background_img.scaled(
            small_w,
            small_h,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.preview_img = self.generate_preview(140, 200)

    def generate_preview(self, w, h):
        preview = QPixmap(w, h)
        painter = QPainter(preview)

        painter.drawPixmap(0, 0, w, h, self.background_img)
        scaled_pipe = self.pipe_img.scaledToWidth(int(w * 0.3))
        pipe_x = w - scaled_pipe.width() - 10
        pipe_y = h - scaled_pipe.height() + 50
        painter.drawPixmap(pipe_x, pipe_y, scaled_pipe)

        scaled_bird = self.bird_img.scaledToWidth(int(w * 0.3))
        bird_x = (w - scaled_bird.width()) // 2
        bird_y = (h - scaled_bird.height()) // 2
        painter.drawPixmap(bird_x, bird_y, scaled_bird)

        painter.end()

        return preview
