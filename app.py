import streamlit as st
from PIL import Image
import numpy as np

# 👉 import your existing emotion logic
# emotion_music_player.py MUST have a function:
# def detect_emotion(image): return emotion_string
from emotion_music_player import detect_emotion  

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Emotion Music Player",
    page_icon="🎧",
    layout="wide"
)

# -------------------- CSS --------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Title */
.title {
    font-size: 60px;
    font-weight: 800;
    letter-spacing: 2px;
    animation: fadeIn 1.5s ease-in-out;
}

/* Subtitle */
.subtitle {
    font-size: 20px;
    color: #bbbbbb;
    margin-bottom: 30px;
}

/* Card */
.card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
    animation: slideUp 1.2s ease;
}

/* Scan Button */
.scan-btn button {
    background: linear-gradient(90deg, #1DB954, #1ED760);
    color: black !important;
    font-size: 22px !important;
    font-weight: bold;
    padding: 12px 30px !important;
    border-radius: 50px !important;
    transition: 0.3s ease-in-out;
    animation: pulse 2s infinite;
}

/* Hover */
.scan-btn button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 25px #1DB954;
}

/* Animations */
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

@keyframes slideUp {
    from {transform: translateY(40px); opacity: 0;}
    to {transform: translateY(0); opacity: 1;}
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(29,185,84,0.7); }
    70% { box-shadow: 0 0 0 18px rgba(29,185,84,0); }
    100% { box-shadow: 0 0 0 0 rgba(29,185,84,0); }
}

</style>
""", unsafe_allow_html=True)

# -------------------- UI --------------------
st.markdown("<div class='title'>🎧 Emotion Music Player</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your AI-powered Spotify, that feels your mood</div>", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([1.2, 1.8])

# ---------------- LEFT SIDE — SCANNER ----------------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🎭 Face Emotion Scanner")
    st.write("Click below and allow camera access.")

    st.markdown("<div class='scan-btn'>", unsafe_allow_html=True)
    scan_clicked = st.button("📷 Scan My Face")
    st.markdown("</div>", unsafe_allow_html=True)

    if scan_clicked:
        st.info("Camera will open below 👇 Please allow permission")

    # ✅ Browser-based camera (THIS WORKS ONLINE)
    img = st.camera_input("Take a photo")

    if img is not None:
        image = Image.open(img)
        image = np.array(image)

        emotion = detect_emotion(image)
        st.success(f"Detected Emotion: {emotion}")

        # 🎵 Play music in browser
        if emotion.lower() == "happy":
            st.audio("music/game3/happy/happy.mp3")
        elif emotion.lower() == "sad":
            st.audio("music/game3/sad/sad.mp3")
        else:
            st.audio("music/game3/calm/calm.mp3")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RIGHT SIDE — INFO ----------------
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🎶 How It Works")
    st.markdown("""
    ✅ Click **Scan My Face**  
    ✅ Browser camera opens  
    ✅ AI detects facial emotion  
    ✅ Music plays instantly  

    ---
    **Supported Emotions:**  
    😊 Happy  
    😢 Sad  
    😐 Neutral  
    😡 Angry  
    😱 Fear  
    """)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- FOOTER ----------------
st.markdown(
    "<center style='color:#aaa;'>🚀 Built with Python • Streamlit • OpenCV • Deep Learning</center>",
    unsafe_allow_html=True
)
