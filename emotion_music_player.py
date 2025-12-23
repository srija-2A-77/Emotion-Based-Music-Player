import os
import random
import cv2
from deepface import DeepFace
import pygame

# ---------------- CONFIG ----------------
MUSIC_DIR = "music"

# FIXED mapping
EMOTION_TO_FOLDER = {
    "happy": "happy",
    "sad": "sad",
    "angry": "angry",
    "fear": "fear",
    "surprise": "surprise",
    "disgust": "disgust",
    "neutral": "neutral"   # neutral emotion
}

# ---------------- INIT ----------------
pygame.mixer.init()

def play_music(emotion):
    folder = EMOTION_TO_FOLDER.get(emotion)

    if folder is None:
        print("Unknown emotion:", emotion)
        return None

    path = os.path.join(MUSIC_DIR, folder)

    if not os.path.exists(path):
        print("❌ Folder not found:", path)
        return None

    songs = [
        f for f in os.listdir(path)
        if f.lower().endswith((".mp3", ".wav"))
    ]

    if not songs:
        print("❌ No songs in:", path)
        return None

    song = random.choice(songs)
    song_path = os.path.join(path, song)

    pygame.mixer.music.stop()
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

    print(f"▶ Playing [{emotion}] -> {song}")
    return song


def run_emotion_player():
    cap = cv2.VideoCapture(0)

    last_emotion = None
    current_song = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.analyze(
                frame,
                actions=["emotion"],
                enforce_detection=False
            )

            emotion = result[0]["dominant_emotion"]

            # DEBUG PRINT ✅
            print("Detected emotion:", emotion)

            if emotion != last_emotion:
                last_emotion = emotion
                current_song = play_music(emotion)

            # UI display
            cv2.putText(frame, f"Emotion: {emotion}", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

            if current_song:
                cv2.putText(frame, f"Playing: {current_song}", (20, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

        except Exception as e:
            cv2.putText(frame, "No face detected", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Emotion Music Player", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.music.stop()


if __name__ == "__main__":
    run_emotion_player()
