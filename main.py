import cv2
import mediapipe as mp
import pygame
import time
import math
import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk

# ================== ALARM ==================
pygame.mixer.init()
pygame.mixer.music.load("mixkit-alert-alarm-1005.wav")

# ================== MEDIAPIPE ==================
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)

# ================== CAMERA ==================
cap = cv2.VideoCapture(0)
print("Camera opened:", cap.isOpened())

# ================== GUI ==================
root = tk.Tk()
root.title("Drowsiness Monitoring System")

status_lbl = tk.Label(root, text="Status: Awake", font=("Arial", 16))
status_lbl.pack(pady=5)

score_lbl = tk.Label(root, text="Score: 0%", font=("Arial", 14))
score_lbl.pack()

progress = ttk.Progressbar(root, length=300, maximum=100)
progress.pack(pady=10)

# ================== PARAMETERS ==================
EYE_CLOSE_TIME = 2.5
start_time = None
alarm_on = False

score = 0
MAX_SCORE = 100

# ================== LOG FILE ==================
log_file = open("drowsiness_log.csv", "a", newline="")
writer = csv.writer(log_file)
writer.writerow(["time", "score", "status"])

# ================== UTILS ==================
def dist(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

# ================== MAIN LOOP ==================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        face = results.multi_face_landmarks[0]

        h, w, _ = frame.shape

        # ----------- EYES -----------
        top = face.landmark[159]
        bottom = face.landmark[145]
        eye_val = dist(top, bottom)

        # ----------- MOUTH / YAWN -----------
        mouth_top = face.landmark[13]
        mouth_bottom = face.landmark[14]
        mouth_open = dist(mouth_top, mouth_bottom)

        # ----------- HEAD POSE -----------
        nose = face.landmark[1]
        chin = face.landmark[152]
        head_drop = chin.y - nose.y

        # ----------- DRAW VALUES -----------
        cv2.putText(frame, f"Eye:{eye_val:.4f}", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # ----------- SCORE UPDATES -----------

        # Yawning
        if mouth_open > 0.04:
            cv2.putText(frame, "Yawning!", (300, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2)
            score += 3

        # Head down
        if head_drop > 0.18:
            cv2.putText(frame, "Head Down!", (300, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 255), 2)
            score += 2

        # Eye closed
        if eye_val < 0.015:
            if start_time is None:
                start_time = time.time()
            elif time.time() - start_time > EYE_CLOSE_TIME:

                cv2.putText(frame, "DROWSY !!!",
                            (120, 140),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.6, (0, 0, 255), 4)

                score += 2

                if not alarm_on:
                    pygame.mixer.music.play(-1)
                    alarm_on = True

                    writer.writerow([
                        datetime.now().strftime("%H:%M:%S"),
                        score,
                        "DROWSY"
                    ])
        else:
            start_time = None
            if alarm_on:
                pygame.mixer.music.stop()
                alarm_on = False
            score -= 1

        # Clamp score
        score = max(0, min(score, MAX_SCORE))

        # ----------- SHOW SCORE ----------
        cv2.putText(frame, f"Sleepiness: {score}%",
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 255, 255), 2)

        # ----------- GUI UPDATE ----------
        progress["value"] = score
        score_lbl.config(text=f"Score: {score}%")

        if score > 60:
            status_lbl.config(text="Status: DROWSY")
        else:
            status_lbl.config(text="Status: Awake")

        root.update()

    cv2.imshow("Drowsiness Detector - Advanced", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ================== CLEANUP ==================
log_file.close()
cap.release()
cv2.destroyAllWindows()
root.destroy()
