import os
import sys
import numpy as np
import cv2
from audio_player import AudioPlayer, PHRASES
from gesture_detector import GestureDetector

def test_audio():
    print("[TEST 1/2] Memeriksa semua audio (Halo, Nama aku, Reziao, See you, Lengkap)...")
    for key, data in PHRASES.items():
        assert data["file"].exists(), f"File {data['file']} belum ada!"
        assert data["file"].stat().st_size > 0, f"File {data['file']} kosong!"
        print(f"  [OK] Audio {key} siap ({data['file'].stat().st_size} bytes)")
    player = AudioPlayer()
    print("  [OK] Inisialisasi AudioPlayer & preloaded sound berhasil.")

def test_detector():
    print("\n[TEST 2/2] Memeriksa GestureDetector dengan deteksi hijau dan model_complexity=0...")
    detector = GestureDetector()
    dummy_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    processed, raw, confirmed = detector.process(dummy_frame)
    assert processed.shape == (720, 1280, 3)
    assert raw == "NONE"
    print("  [OK] MediaPipe Hands, Green Cyber Mesh, dan Ratio Classifier siap.")

if __name__ == "__main__":
    test_audio()
    test_detector()
    print("\n=== SEMUA VALIDASI 100% SUKSES ===")
