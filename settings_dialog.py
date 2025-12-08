from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class SettingsDialog(QDialog):
    def __init__(self, parent, sound_manager, config):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(380, 220)  # Чуть шире для красоты
        self.sound_manager = sound_manager
        self.config = config

        # Стилизация
        self.setStyleSheet("""
            QDialog { background-color: #333; color: white; }
            QLabel { color: white; font-size: 14px; font-weight: bold; border: none; }

            /* Слайдеры */
            QSlider::groove:horizontal {
                border: 1px solid #999; height: 8px; background: #555; margin: 2px 0; border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #E0C068; border: 1px solid #5c5c5c; width: 18px; margin: -2px 0; border-radius: 9px;
            }
            QSlider:disabled { background: #444; }

            /* Кнопки-иконки (прозрачные, большие) */
            QPushButton.iconBtn {
                background: transparent; border: none; font-size: 24px; text-align: center;
            }
            QPushButton.iconBtn:hover { color: #E0C068; }

            /* Обычные кнопки */
            QPushButton.actionBtn {
                background-color: #E0C068; border-radius: 5px; font-weight: bold; color: #333;
            }
            QPushButton.actionBtn:hover { background-color: #F0D078; }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 30, 20, 20)

        # --- СТРОКА МУЗЫКИ ---
        layout.addLayout(
            self.create_slider_row(
                "Music",
                self.sound_manager.music_vol,
                self.sound_manager.is_music_muted,
                self.toggle_music_mute,
                self.update_music_vol,
                "btn_music",
            )
        )

        # --- СТРОКА ЭФФЕКТОВ ---
        layout.addLayout(
            self.create_slider_row(
                "SFX",
                self.sound_manager.sfx_vol,
                self.sound_manager.is_sfx_muted,
                self.toggle_sfx_mute,
                self.update_sfx_vol,
                "btn_sfx",
            )
        )

        layout.addStretch(1)

        # --- КНОПКА OK ---
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.setProperty("class", "actionBtn")  # Для CSS
        ok_btn.setFixedSize(100, 40)
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)

    def create_slider_row(
        self, label_text, current_vol, is_muted, mute_handler, vol_handler, btn_name
    ):
        """Вспомогательный метод для создания ровной строки"""
        row = QHBoxLayout()

        # 1. Кнопка Mute (Иконка)
        btn = QPushButton("🔇" if is_muted else "🔊")
        btn.setObjectName("iconBtn")  # Стиль
        btn.setFixedWidth(40)
        btn.clicked.connect(mute_handler)
        # Сохраняем ссылку на кнопку в self, чтобы менять иконку позже
        setattr(self, btn_name, btn)
        row.addWidget(btn)

        # 2. Текст (Фиксированная ширина = ровные слайдеры!)
        lbl = QLabel(label_text)
        lbl.setFixedWidth(60)  # <--- ВОТ РЕШЕНИЕ ПРОБЛЕМЫ С ДЛИНОЙ
        row.addWidget(lbl)

        # 3. Слайдер
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(int(current_vol * 100))
        slider.valueChanged.connect(vol_handler)

        # Сохраняем ссылку на слайдер (slider_music или slider_sfx)
        setattr(self, f"slider_{label_text.lower()}", slider)

        row.addWidget(slider)
        return row

    # --- ЛОГИКА ---

    def toggle_music_mute(self):
        new_state = not self.sound_manager.is_music_muted
        self.sound_manager.mute_music(new_state)
        self.config["audio"]["music_muted"] = new_state

        # Обновляем UI
        self.btn_music.setText("🔇" if new_state else "🔊")
        self.slider_music.setEnabled(not new_state)

    def toggle_sfx_mute(self):
        new_state = not self.sound_manager.is_sfx_muted
        self.sound_manager.mute_sfx(new_state)
        self.config["audio"]["sfx_muted"] = new_state

        # Обновляем UI
        self.btn_sfx.setText("🔇" if new_state else "🔊")
        self.slider_sfx.setEnabled(not new_state)

    def update_music_vol(self, value):
        vol = value / 100.0
        self.sound_manager.set_music_volume(vol)
        self.config["audio"]["music_volume"] = vol

    def update_sfx_vol(self, value):
        vol = value / 100.0
        self.sound_manager.set_sfx_volume(vol)
        self.config["audio"]["sfx_volume"] = vol
