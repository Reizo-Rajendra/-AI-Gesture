import os
import sys
import time
import cv2
import numpy as np
from audio_player import AudioPlayer
from gesture_detector import GestureDetector

def draw_rounded_rect(img, pt1, pt2, color, thickness=-1, radius=14):
    """Menggambar kotak rounded bersudut halus untuk subtitle banner."""
    x1, y1 = pt1
    x2, y2 = pt2
    w = x2 - x1
    h = y2 - y1

    if w <= 0 or h <= 0:
        return

    radius = min(radius, w // 2, h // 2)

    if thickness == -1:
        cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, -1)
        cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, -1)
        cv2.circle(img, (x1 + radius, y1 + radius), radius, color, -1)
        cv2.circle(img, (x2 - radius, y1 + radius), radius, color, -1)
        cv2.circle(img, (x1 + radius, y2 - radius), radius, color, -1)
        cv2.circle(img, (x2 - radius, y2 - radius), radius, color, -1)
    else:
        cv2.line(img, (x1 + radius, y1), (x2 - radius, y1), color, thickness)
        cv2.line(img, (x1 + radius, y2), (x2 - radius, y2), color, thickness)
        cv2.line(img, (x1, y1 + radius), (x1, y2 - radius), color, thickness)
        cv2.line(img, (x2, y1 + radius), (x2, y2 - radius), color, thickness)
        cv2.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)
        cv2.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)

def draw_cyber_subtitle_banner(frame, text):
    """
    Menggambar banner subtitle futuristik satu-satu (tampil hanya saat ada kata aktif).
    """
    if not text:
        return frame

    h, w, _ = frame.shape
    font_main = cv2.FONT_HERSHEY_DUPLEX
    font_tech = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.15
    font_thickness = 2

    (text_w, text_h), baseline = cv2.getTextSize(text, font_main, font_scale, font_thickness)

    pad_x = 32
    pad_top = 28
    pad_bottom = 18
    header_h = 16
    box_w = max(text_w + pad_x * 2, 320)
    box_h = text_h + pad_top + pad_bottom + header_h

    x1 = max(10, (w - box_w) // 2)
    y1 = 28
    x2 = min(w - 10, x1 + box_w)
    y2 = y1 + box_h

    # Layer transparan hitam elegan
    overlay = frame.copy()
    draw_rounded_rect(overlay, (x1, y1), (x2, y2), (18, 18, 22), thickness=-1, radius=14)
    # Border neon hijau-cyan berkilau
    draw_rounded_rect(overlay, (x1, y1), (x2, y2), (0, 255, 180), thickness=2, radius=14)

    alpha = 0.88
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Header kecil: ● ACTIVE GESTURE
    stage_header = "AI GESTURE  |  ● ACTIVE PHRASE"
    cv2.putText(frame, stage_header, (x1 + pad_x, y1 + 18), font_tech, 0.42, (0, 255, 200), 1, cv2.LINE_AA)

    # Teks utama satu-satu putih tajam
    text_x = x1 + (box_w - text_w) // 2
    text_y = y1 + pad_top + header_h + text_h - 4
    cv2.putText(frame, text, (text_x, text_y), font_main, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

    return frame

def main():
    print("=" * 65)
    print("  PERKENALAN DIRI INTERAKTIF - REIZO RAJENDRA DIANTA")
    print("  Mode Satu-Satu + Auto-Hide + Reset Mengepal")
    print("=" * 65)

    audio = AudioPlayer()
    detector = GestureDetector(confirm_frames=2)

    print("\n[Kamera] Menghubungkan ke webcam...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[Kamera] Index 0 gagal, mencoba index 1...")
        cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("[Error] Webcam tidak dapat dibuka! Pastikan tidak sedang digunakan aplikasi lain.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    window_name = "Perkenalan Diri Interaktif"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # Variabel status tampilan satu-satu
    active_text = ""
    text_expire_time = 0.0
    TEXT_DURATION = 3.0  # Teks tampil selama 3 detik lalu otomatis hilang agar bersih
    has_said_name = False

    print("\n[Panduan Gestur Satu-Satu & Respon Cepat]:")
    print("  1. 🖐️  5 Jari Terbuka       -> Tampil & Suara: 'Halo'")
    print("  2. ✌️  2 Jari (Peace) / ☝️   -> Tampil & Suara: 'Nama aku'")
    print("  3. 🤟  Metal 3 Jari (Love)  -> Tampil & Suara: 'Reizo Rajendra Dianta'")
    print("  4. 🤙 / 🖐️  Shaka / Melambai -> Tampil & Suara: 'See you!'")
    print("  [Selesai] ✊ Mengepal       -> Teks LANGSUNG HILANG TOTAL dari layar!")
    print("  Tekan 'q' untuk keluar.\n")

    while True:
        success, frame = cap.read()
        if not success:
            time.sleep(0.03)
            continue

        frame = cv2.flip(frame, 1)

        # Proses deteksi tangan + titik hijau bercahaya + jaring 3D
        frame, raw_gesture, confirmed_trigger = detector.process(frame)

        now = time.time()

        # -------------------------------------------------------------
        # Pemicu Gestur Satu-Satu (Respon Ultra-Cepat)
        # -------------------------------------------------------------
        if confirmed_trigger == "FIST":
            # Saat mengepal selesai: teks langsung HILANG TOTAL dari layar!
            if active_text or has_said_name:
                print(">>> [MENGEPAL SELESAI] Teks di atas langsung hilang bersih!")
                active_text = ""
                text_expire_time = 0.0
                has_said_name = False

        elif confirmed_trigger == "LOVE_SIGN":
            print(">>> [REIZO] Gestur Metal 3 Jari -> 'Reizo Rajendra Dianta'")
            active_text = "Reizo Rajendra Dianta"
            text_expire_time = now + 3.5
            has_said_name = True
            audio.speak("REIZO")

        elif confirmed_trigger == "PEACE":
            print(">>> [NAMA AKU] Gestur 2 Jari Peace -> 'Nama aku'")
            active_text = "Nama aku"
            text_expire_time = now + TEXT_DURATION
            audio.speak("NAMA_AKU")

        elif confirmed_trigger == "PALM_OPEN":
            # Jika nama sudah pernah diucapkan, melambaikan tangan berarti "See you!"
            if has_said_name:
                print(">>> [SEE YOU] 5 Jari Melambai Akhir -> 'See you!'")
                active_text = "See you!"
                text_expire_time = now + TEXT_DURATION
                audio.speak("SEE_YOU")
            else:
                print(">>> [HALO] 5 Jari Awal -> 'Halo'")
                active_text = "Halo"
                text_expire_time = now + TEXT_DURATION
                audio.speak("HALO")

        elif confirmed_trigger == "SHAKA":
            print(">>> [SEE YOU] Gestur Shaka -> 'See you!'")
            active_text = "See you!"
            text_expire_time = now + TEXT_DURATION
            audio.speak("SEE_YOU")

        # Cek apakah durasi tampil teks sudah habis (hilang otomatis agar tidak ada terus)
        if now > text_expire_time:
            active_text = ""

        # Gambar Banner Subtitle HANYA jika ada teks aktif (jika hilang, layar bersih total!)
        if active_text:
            draw_cyber_subtitle_banner(frame, active_text)

        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            print("[Info] Keluar dari program.")
            break
        elif key == ord('c'):
            print("[Reset] Teks dibersihkan.")
            active_text = ""
            text_expire_time = 0.0
            has_said_name = False

    cap.release()
    cv2.destroyAllWindows()
    print("[Selesai] Kamera ditutup.")

if __name__ == "__main__":
    main()
