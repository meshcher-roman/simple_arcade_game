import os

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer, QSoundEffect


class SoundManager:
    def __init__(self, config):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sound_dir = os.path.join(base_dir, "assets", "sounds")

        audio_cfg = config.get("audio", {})
        self.music_vol = audio_cfg.get("music_volume", 0.5)
        self.sfx_vol = audio_cfg.get("sfx_volume", 1.0)

        self.jump_sfx = self._load_sfx("jump.wav")
        self.score_sfx = self._load_sfx("score.wav")
        self.hit_sfx = self._load_sfx("hit.wav")

        self.music_player = QMediaPlayer()
        self.audio_output = QAudioOutput()

        self.music_player.setAudioOutput(self.audio_output)

        self.audio_output.setVolume(self.music_vol)

        music_path = os.path.join(self.sound_dir, "music.wav")
        if os.path.exists(music_path):
            self.music_player.setSource(QUrl.fromLocalFile(music_path))
            self.music_player.setLoops(QMediaPlayer.Loops.Infinite)
        else:
            print(f"Warning: Music file not found: {music_path}")

    def _load_sfx(self, filename):
        """Загрузка коротких эффектов"""
        path = os.path.join(self.sound_dir, filename)
        if not os.path.exists(path):
            print(f"Warning: SFX file not found: {path}")
            return None

        effect = QSoundEffect()
        effect.setSource(QUrl.fromLocalFile(path))
        effect.setVolume(self.sfx_vol)
        return effect

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
        # QMediaPlayer управляется иначе
        if self.music_player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
            self.music_player.play()

    def stop_music(self):
        if self.music_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.music_player.stop()
