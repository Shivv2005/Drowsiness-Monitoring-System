# Drowsiness-Monitoring-System

🚗 Drowsiness Monitoring System 

A real-time computer vision–based application that detects signs of fatigue by analyzing facial landmarks from a live webcam feed. The system monitors eye closure duration, yawning frequency, and head posture to calculate a dynamic sleepiness score, trigger alarm alerts, and log drowsiness events for later analysis. This project demonstrates how AI-powered vision systems can be applied to safety-critical domains such as driver monitoring and smart surveillance.

✨ Features

Real-time webcam-based fatigue detection

Facial landmark tracking using Face Mesh

Eye-closure timing for microsleep detection

Yawn detection through mouth landmarks

Head-tilt monitoring

Multi-factor sleepiness scoring system

Tkinter GUI dashboard with progress bar and status label

Alarm alert using sound playback

CSV logging with timestamps

Live video feed with metric overlays

Modular and extensible Python codebase

🛠️ Tech Stack

Python

OpenCV

MediaPipe

Tkinter

Pygame

📂 Project Structure
📁 drowsiness-monitoring-system/
│
├── main.py                 # Core detection logic
├── mixkit-alert-alarm.wav  # Alarm sound file
├── drowsiness_log.csv      # Generated log file
├── README.md               # Project documentation



Install required packages:

pip install opencv-python mediapipe pygame

▶️ How to Run
python main.py


Make sure:

Your webcam is connected

The alarm .wav file is in the same directory

Press ESC to exit the application.

📊 How It Works

Captures live video frames from the webcam

Detects facial landmarks

Measures eye opening, mouth opening, and head position

Updates a sleepiness score

Plays an alarm when the threshold is crossed

Logs events into a CSV file

Displays results in both OpenCV and GUI windows

🚀 Use Cases

Driver alertness monitoring systems

Road safety applications

Smart surveillance

Academic projects and research

Human fatigue analysis

🔮 Future Enhancements

Machine learning–based classifier

User-specific calibration

Mobile or embedded deployment

Cloud-based logging dashboard

Multiple-face tracking

Dataset generation & training pipeline

📜 License

This project is released for educational and research purposes.
