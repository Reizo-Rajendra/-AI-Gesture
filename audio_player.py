import os
import sys
import time
import threading
from pathlib import Path
from gtts import gTTS
import pygame

AUDIO_DIR = Path(__file__).parent / "audio"
AUDIO_DIR.mkdir(exist_ok=True)

PHRASES = {
    "HALO": {
        "text": "Halo",
        "file": AUDIO_DIR / "halo.mp3",
        "lang": "id"
    },
    "NAMA_AKU": {
        "text": "Nama aku",
        "file": AUDIO_DIR / "nama_aku.mp3",
        "lang": "id"
    },
    "REIZO": {
        "text": "Reizo Rajendra Dianta",
        "file": AUDIO_DIR / "reizo.mp3",
        "lang": "id"
    },
    "SEE_YOU": {
        "text": "See you!",
        "file": AUDIO_DIR / "see_you.mp3",
        "lang": "en"
    },
    "LENGKAP": {
        "text": "Halo, nama aku Reizo Rajendra Dianta. See you!",
        "file": AUDIO_DIR / "lengkap.mp3",
        "lang": "id"
    }
}

class AudioPlayer:
    def __init__(self):
        self.mixer_ready = False
        self.sounds = {}
        self.last_spoken_key = None
        self.last_spoken_time = 0.0
        self.cooldown = 0.8
        
        self._init_mixer()
        self._pregenerate_audio()
        self._load_sounds()

    def _init_mixer(self):
        try:
            pygame.mixer.pre_init(44100, -16, 2, 1024)
            pygame.mixer.init()
            pygame.mixer.set_num_channels(8)
            self.mixer_ready = True
            print("[AudioPlayer] Pygame Mixer aktif.")
        except Exception as e:
            print(f"[AudioPlayer] Mixer gagal: {e}")
            self.mixer_ready = False

    def _pregenerate_audio(self):
        for key, item in PHRASES.items():
            filepath = item["file"]
            if not filepath.exists() or filepath.stat().st_size == 0:
                print(f"[AudioPlayer] Mengunduh: '{item['text']}' -> {filepath.name}")
                try:
                    tts = gTTS(text=item["text"], lang=item.get("lang", "id"), slow=False)
                    tts.save(str(filepath))
                except Exception as e:
                    print(f"[AudioPlayer] GTTS error: {e}")
                    self._generate_offline(item["text"], filepath)

    def _generate_offline(self, text, filepath):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file(text, str(filepath))
            engine.runAndWait()
        except Exception as err:
            print(f"[AudioPlayer] Fallback error: {err}")

    def _load_sounds(self):
        if not self.mixer_ready:
            return
        for key, item in PHRASES.items():
            filepath = item["file"]
            if filepath.exists():
                try:
                    snd = pygame.mixer.Sound(str(filepath))
                    snd.set_volume(1.0)
                    self.sounds[key] = snd
                except Exception as e:
                    print(f"[AudioPlayer] Gagal memuat sound {key}: {e}")

    def speak(self, phrase_key: str):
        now = time.time()
        if phrase_key == self.last_spoken_key and (now - self.last_spoken_time) < self.cooldown:
            return

        self.last_spoken_key = phrase_key
        self.last_spoken_time = now

        if phrase_key not in PHRASES:
            return

        phrase_data = PHRASES[phrase_key]
        text = phrase_data["text"]
        filepath = phrase_data["file"]

        print(f"Executing speak for: {text} | File: {filepath.name}")

        def _play_worker():
            try:
                if self.mixer_ready and phrase_key in self.sounds:
                    snd = self.sounds[phrase_key]
                    channel = snd.play()
                    while channel and channel.get_busy():
                        time.sleep(0.04)
                    print(f"Successfully finished speak: {text}")
                elif filepath.exists():
                    pygame.mixer.music.load(str(filepath))
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.04)
                else:
                    import pyttsx3
                    engine = pyttsx3.init()
                    engine.say(text)
                    engine.runAndWait()
            except Exception as e:
                print(f"[AudioPlayer] Playback error: {e}")

        thread = threading.Thread(target=_play_worker, daemon=True)
        thread.start()

if __name__ == "__main__":
    player = AudioPlayer()
    player.speak("REIZO")
    time.sleep(2)
