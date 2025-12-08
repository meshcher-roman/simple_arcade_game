import os

from PyQt6.QtCore import QObject, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer, QSoundEffect


class SoundManager(QObject):
    def __init__(self, config):
        super().__init__()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sound_dir = os.path.join(base_dir, "assets", "sounds")

        audio_cfg = config.get("audio", {})
        self.music_vol = audio_cfg.get("music_volume", 0.5)
        self.sfx_vol = audio_cfg.get("sfx_volume", 1.0)

        # НОВОЕ: Загружаем состояние Mute (по умолчанию False - звук включен)
        self.is_music_muted = audio_cfg.get("music_muted", False)
        self.is_sfx_muted = audio_cfg.get("sfx_muted", False)

        # --- 1. SFX (Короткие звуки) ---
        self.jump_sfx = self._load_sfx("jump.wav")
        self.score_sfx = self._load_sfx("score.wav")
        self.hit_sfx = self._load_sfx("hit.wav")

        # Применяем начальное состояние mute для SFX
        self.mute_sfx(self.is_sfx_muted)

        # --- 2. МУЗЫКА (Длинный трек) ---
        self.music_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)

        self.music_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(self.music_vol)
        # Применяем начальное состояние mute для музыки
        self.audio_output.setMuted(self.is_music_muted)

        music_path = os.path.join(self.sound_dir, "music.wav")
        if os.path.exists(music_path):
            self.music_player.setSource(QUrl.fromLocalFile(music_path))
            self.music_player.setLoops(QMediaPlayer.Loops.Infinite)
        else:
            print(f"Warning: Music file not found: {music_path}")

    def _load_sfx(self, filename):
        path = os.path.join(self.sound_dir, filename)
        if not os.path.exists(path):
            return None
        effect = QSoundEffect(self)
        effect.setSource(QUrl.fromLocalFile(path))
        # Громкость ставим базовую, mute наложится позже
        effect.setVolume(self.sfx_vol)
        return effect

    # --- МЕТОДЫ УПРАВЛЕНИЯ ГРОМКОСТЬЮ И MUTE ---

    def set_music_volume(self, volume):
        self.music_vol = volume
        self.audio_output.setVolume(volume)

    def set_sfx_volume(self, volume):
        self.sfx_vol = volume
        # Если звук не заглушен, применяем новую громкость.
        # Если заглушен - только запоминаем её, но оставляем реальную громкость 0.
        if not self.is_sfx_muted:
            if self.jump_sfx:
                self.jump_sfx.setVolume(volume)
            if self.score_sfx:
                self.score_sfx.setVolume(volume)
            if self.hit_sfx:
                self.hit_sfx.setVolume(volume)

    def mute_music(self, mute: bool):
        """Включает/выключает звук музыки"""
        self.is_music_muted = mute
        self.audio_output.setMuted(mute)

    def mute_sfx(self, mute: bool):
        """Включает/выключает звуковые эффекты"""
        self.is_sfx_muted = mute
        # Для QSoundEffect нет встроенного mute, поэтому ставим громкость в 0 или восстанавливаем
        target_vol = 0.0 if mute else self.sfx_vol

        if self.jump_sfx:
            self.jump_sfx.setVolume(target_vol)
        if self.score_sfx:
            self.score_sfx.setVolume(target_vol)
        if self.hit_sfx:
            self.hit_sfx.setVolume(target_vol)

    # --- МЕТОДЫ ВОСПРОИЗВЕДЕНИЯ (без изменений) ---

    def play_jump(self):
        if self.jump_sfx:
            self.jump_sfx.play()

    def play_score(self):
        if self.score_sfx:
            self.score_sfx.play()

    def play_hit(self):
        if self.hit_sfx:
            if not self.hit_sfx.isPlaying():
                self.hit_sfx.play()

    def start_music(self):
        if self.music_player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
            self.music_player.play()

    def stop_music(self):
        if self.music_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.music_player.stop()
