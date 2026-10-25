# AI Hand Gesture Recognition & Interactive Speech
### 🚀 Perkenalan Diri Interaktif — Reizo Rajendra Dianta

Sistem Computer Vision interaktif berbasis **Python**, **OpenCV**, **MediaPipe Hands**, dan **Text-to-Speech (gTTS & Pygame)** untuk mengenalkan diri melalui gestur tangan di depan kamera secara *real-time*.

---

## ✨ Fitur Unggulan

- ⚡ **Respon Ultra-Cepat (< 0.1 Detik)**: Menggunakan algoritma rasio sendi biologis (*Palm-Size Normalized*) yang sangat peka terhadap pencahayaan ruangan dan kamera laptop.
- 🟢 **Cybernetic Hand Mesh 3D**: Menampilkan titik-titik sendi hijau neon berkilau, jaring-jaring 3D (*webbing* antar ruas jari), dan *Cyber Target Ring* di tengah telapak tangan.
- 🗣️ **Suara Jernih Bahasa Indonesia**: Menggunakan audio *pre-loaded* yang diputar di *background thread* tanpa membebani performa *framerate* kamera (30+ FPS mulus).
- 🧼 **Layar Bersih & Tampilan Satu-Satu**: Teks subtitle muncul elegan di atas hanya saat kata diucapkan, lalu otomatis menghilang setelah 3 detik.
- ✊ **Reset Cepat dengan Mengepal**: Kapan saja tangan mengepal (selesai), teks di atas langsung hilang seketika!

---

## 🖐️ Panduan Gestur Tangan

| Gestur | Visual Tangan | Teks yang Tampil | Suara yang Terdengar |
|:---:|:---|:---|:---|
| **1** | 🖐️ **5 Jari Terbuka** | `Halo` | *"Halo"* |
| **2** | ✌️ **2 Jari Peace / ☝️ 1 Jari** | `Nama aku` | *"Nama aku"* |
| **3** | 🤟 **Metal 3 Jari / Love Sign** | `Reizo Rajendra Dianta` | *"Reizo Rajendra Dianta"* |
| **4** | 🤙 **Shaka / 🖐️ Melambai di Akhir** | `See you!` | *"See you!"* |
| **Reset** | ✊ **Mengepal (Fist) / Tekan 'C'** | *(Teks langsung hilang bersih)* | - |

---

## 🛠️ Instalasi & Persyaratan

Pastikan Anda telah memasang **Python 3.11** pada sistem Anda.

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/Reizo-Rajendra/-AI-Gesture.git
   cd -AI-Gesture
   ```

2. **Buat dan aktifkan virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   ```

3. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Cara Menjalankan

### Cara 1: Sekali Klik (Windows)
Cukup klik dua kali file:
```
run.bat
```

### Cara 2: Dari VS Code
1. Buka folder proyek di Visual Studio Code.
2. Buka file `main.py`.
3. Tekan **`F5`** atau klik tombol **Play (▶️)** di pojok kanan atas.

### Cara 3: Melalui Terminal
```bash
python main.py
```

---

## ⌨️ Tombol Pintas Keyboard
- **`q`** atau **`Esc`**: Menutup dan keluar dari kamera.
- **`c`**: Menghapus teks di layar secara manual.

---

## 📄 Lisensi
Dilisensikan di bawah [MIT License](LICENSE).
