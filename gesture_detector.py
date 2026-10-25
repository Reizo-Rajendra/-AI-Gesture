import math
import cv2
import numpy as np
import mediapipe as mp

class GestureDetector:
    def __init__(self, min_detection_confidence=0.15, min_tracking_confidence=0.15, confirm_frames=2):
        self.mp_hands = mp.solutions.hands
        # model_complexity=0 sangat peka dan responsif untuk webcam laptop
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

        # Hanya butuh 2 frame (~0.06 detik) agar respon INSTAN
        self.confirm_frames = confirm_frames
        self.current_candidate = None
        self.candidate_frames = 0
        self.last_triggered_gesture = None
        self.anim_frame = 0

    def _calc_distance(self, p1, p2):
        """Menghitung jarak Euclidean 2D antar titik landmark normalisasi."""
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def classify_gesture(self, landmarks):
        """
        Klasifikasi gestur tangan ultra responsif dan akurat:
        - LOVE_SIGN (🤟 / 🤘 Metal Sign)
        - PEACE (✌️ 2 Jari / ☝️ 1 Jari)
        - PALM_OPEN (🖐️ 5 Jari)
        - SHAKA (🤙 Shaka)
        - FIST (✊ Mengepal)
        """
        lm = landmarks
        palm_size = self._calc_distance(lm[0], lm[9])
        if palm_size < 0.03:
            return "UNKNOWN"

        # 1. Status Tiap Jari (Apakah Naik atau Tertekuk)
        index_up = (lm[8].y < lm[6].y) or (self._calc_distance(lm[8], lm[0]) > self._calc_distance(lm[6], lm[0]) * 1.05)
        middle_up = (lm[12].y < lm[10].y) or (self._calc_distance(lm[12], lm[0]) > self._calc_distance(lm[10], lm[0]) * 1.05)
        pinky_up = (lm[20].y < lm[18].y) or (self._calc_distance(lm[20], lm[0]) > self._calc_distance(lm[18], lm[0]) * 1.05)
        ring_up = (lm[16].y < lm[14].y) or (self._calc_distance(lm[16], lm[0]) > self._calc_distance(lm[14], lm[0]) * 1.05)

        # Status Tertekuk (Folded)
        middle_folded = (not middle_up) or (lm[12].y > lm[8].y + 0.02)
        ring_folded = (not ring_up) or (lm[16].y > lm[20].y + 0.01)

        # Status Jempol
        dist_thumb_pinky = self._calc_distance(lm[4], lm[17]) / palm_size
        is_thumb_open = dist_thumb_pinky > 0.95

        # -------------------------------------------------------------
        # A. METAL / LOVE SIGN 🤟 atau 🤘:
        # Telunjuk & Kelingking tegak; Tengah & Manis tertekuk
        # -------------------------------------------------------------
        if index_up and pinky_up and middle_folded and ring_folded:
            return "LOVE_SIGN"

        # -------------------------------------------------------------
        # B. PALM OPEN 🖐️ (Semua jari terbuka tegak)
        # -------------------------------------------------------------
        if index_up and middle_up and ring_up and pinky_up:
            return "PALM_OPEN"

        # -------------------------------------------------------------
        # C. PEACE ✌️ (Telunjuk & Tengah tegak) atau POINTING ☝️ (Telunjuk saja)
        # Manis & Kelingking harus tertekuk
        # -------------------------------------------------------------
        if index_up and ring_folded and (not pinky_up):
            return "PEACE"

        # -------------------------------------------------------------
        # D. SHAKA 🤙 (Jempol & Kelingking tegak, 3 jari tengah tertekuk)
        # -------------------------------------------------------------
        if pinky_up and (not index_up) and middle_folded and ring_folded and is_thumb_open:
            return "SHAKA"

        # -------------------------------------------------------------
        # E. FIST ✊ (Semua jari tertekuk)
        # -------------------------------------------------------------
        if (not index_up) and middle_folded and ring_folded and (not pinky_up):
            return "FIST"

        return "UNKNOWN"

    def draw_cyber_effects(self, frame, landmarks):
        """
        Menggambar efek cybernetic neon:
        - Titik hijau terang (0, 255, 0) di setiap sendi
        - Jaring 3D futuristic webbing
        - Cincin bidikan AI (Cyber Target Ring) di tengah telapak
        """
        self.anim_frame += 1
        h, w, _ = frame.shape
        points = []
        for lm in landmarks.landmark:
            cx, cy = int(lm.x * w), int(lm.y * h)
            points.append((cx, cy))

        overlay = frame.copy()

        # 1. Garis Jaring 3D (Webbing antar ruas jari)
        fingertip_indices = [4, 8, 12, 16, 20]
        for i in range(len(fingertip_indices) - 1):
            cv2.line(overlay, points[fingertip_indices[i]], points[fingertip_indices[i + 1]], (0, 255, 200), 1, cv2.LINE_AA)

        pip_indices = [3, 6, 10, 14, 18]
        for i in range(len(pip_indices) - 1):
            cv2.line(overlay, points[pip_indices[i]], points[pip_indices[i + 1]], (0, 220, 255), 1, cv2.LINE_AA)

        mcp_indices = [2, 5, 9, 13, 17]
        for i in range(len(mcp_indices) - 1):
            cv2.line(overlay, points[mcp_indices[i]], points[mcp_indices[i + 1]], (0, 255, 120), 1, cv2.LINE_AA)

        cross_pairs = [(5, 10), (9, 6), (9, 14), (13, 10), (13, 18), (17, 14), (0, 5), (0, 9), (0, 13), (0, 17)]
        for idx1, idx2 in cross_pairs:
            cv2.line(overlay, points[idx1], points[idx2], (140, 240, 255), 1, cv2.LINE_AA)

        # 2. Cincin Target Cyber di Pusat Telapak Tangan
        palm_center_x = int((points[0][0] + points[9][0]) / 2)
        palm_center_y = int((points[0][1] + points[9][1]) / 2)
        radius = int(self._calc_distance(landmarks.landmark[0], landmarks.landmark[9]) * w * 0.45)
        radius = max(18, min(radius, 60))

        cv2.circle(overlay, (palm_center_x, palm_center_y), radius, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.circle(overlay, (palm_center_x, palm_center_y), radius + 6, (0, 255, 120), 1, cv2.LINE_AA)
        cv2.line(overlay, (palm_center_x - radius - 8, palm_center_y), (palm_center_x - radius + 3, palm_center_y), (0, 255, 255), 2, cv2.LINE_AA)
        cv2.line(overlay, (palm_center_x + radius - 3, palm_center_y), (palm_center_x + radius + 8, palm_center_y), (0, 255, 255), 2, cv2.LINE_AA)
        cv2.line(overlay, (palm_center_x, palm_center_y - radius - 8), (palm_center_x, palm_center_y - radius + 3), (0, 255, 255), 2, cv2.LINE_AA)
        cv2.line(overlay, (palm_center_x, palm_center_y + radius - 3), (palm_center_x, palm_center_y + radius + 8), (0, 255, 255), 2, cv2.LINE_AA)

        alpha = 0.55
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        # 3. Tulang Tangan (Putih Bersih)
        connections = self.mp_hands.HAND_CONNECTIONS
        for connection in connections:
            cv2.line(frame, points[connection[0]], points[connection[1]], (255, 255, 255), 2, cv2.LINE_AA)

        # 4. Titik Hijau Neon Terang (0, 255, 0)
        for i, (cx, cy) in enumerate(points):
            cv2.circle(frame, (cx, cy), 6, (0, 255, 0), -1, cv2.LINE_AA)
            cv2.circle(frame, (cx, cy), 2, (255, 255, 255), -1, cv2.LINE_AA)

    def process(self, frame_bgr):
        """Memproses frame secara instan dengan debounce 2 frame (~0.06s)."""
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        raw_gesture = "NONE"
        confirmed_trigger = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.draw_cyber_effects(frame_bgr, hand_landmarks)
                raw_gesture = self.classify_gesture(hand_landmarks.landmark)
                break

            # Respon instan: 2 frame konfirmasi
            if raw_gesture not in ["NONE", "UNKNOWN"]:
                if raw_gesture == self.current_candidate:
                    self.candidate_frames += 1
                else:
                    self.current_candidate = raw_gesture
                    self.candidate_frames = 1

                if self.candidate_frames >= self.confirm_frames:
                    if self.last_triggered_gesture != raw_gesture:
                        confirmed_trigger = raw_gesture
                        self.last_triggered_gesture = raw_gesture
            else:
                self.candidate_frames = 0
                self.current_candidate = None
                self.last_triggered_gesture = None
        else:
            self.candidate_frames = 0
            self.current_candidate = None
            self.last_triggered_gesture = None

        return frame_bgr, raw_gesture, confirmed_trigger
