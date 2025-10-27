# emotion_music_player.py

import os
import random
import cv2
import numpy as np
from deepface import DeepFace
import pygame

# ------------ CONFIG ------------
MUSIC_DIR = "music"  # main music folder
EMOTION_TO_FOLDER = {
    "happy": "happy",
    "sad": "sad",
    "angry": "angry",
    "surprise": "surprise",
    "fear": "fear",
    "disgust": "disgust",
    "neutral": "neutral"
}

# ------------ INIT ------------
pygame.mixer.init()

def play_music(emotion):
    """Play a random song from the folder matching the emotion."""
    folder = EMOTION_TO_FOLDER.get(emotion, "neutral")
    path = os.path.join(MUSIC_DIR, folder)

    if not os.path.exists(path):
        print(f"No folder found for emotion: {emotion}")
        return None

    files = [f for f in os.listdir(path) if f.endswith((".mp3", ".wav"))]
    if not files:
        print(f"No music files in folder: {path}")
        return None

    song = random.choice(files)
    song_path = os.path.join(path, song)

    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

    return song


# ------------ CAMERA LOOP ------------
cap = cv2.VideoCapture(0)

current_song = None
current_emotion = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # Detect emotion
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']

        # If emotion changes → play new song
        if dominant_emotion != current_emotion:
            current_emotion = dominant_emotion
            current_song = play_music(dominant_emotion)

        # Display emotion on screen
        cv2.putText(frame, f"Emotion: {dominant_emotion}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2, cv2.LINE_AA)

        # Display song name if playing
        if current_song:
            cv2.putText(frame, f"Playing: {current_song}", (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2, cv2.LINE_AA)

    except Exception as e:
        cv2.putText(frame, "No face detected", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Show video feed
    cv2.imshow("Emotion Music Player", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
