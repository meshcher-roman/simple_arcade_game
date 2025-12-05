from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap


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
