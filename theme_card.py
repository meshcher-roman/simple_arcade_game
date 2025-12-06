from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget


class ThemeCard(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, theme, index, is_selected=False):
        super().__init__()
        self.theme = theme
        self.index = index
        self.is_selected = is_selected
        self.setFixedSize(140, 200)

    def set_selected(self, selected):
        self.is_selected = selected
        self.update()  # Перерисовать рамку

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.index)

    def paintEvent(self, event):
        painter = QPainter(self)

        # 1. Рисуем сгенерированное превью
        painter.drawPixmap(0, 0, self.width(), self.height(), self.theme.preview_img)

        # 2. Если выбрано - рисуем жирную рамку
        if self.is_selected:
            pen = painter.pen()
            pen.setColor(QColor("#FFD700"))  # Золотой цвет
            pen.setWidth(6)
            painter.setPen(pen)
            # Рисуем прямоугольник внутри границ
            painter.drawRect(3, 3, self.width() - 6, self.height() - 6)

        painter.end()
