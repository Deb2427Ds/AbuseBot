import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr
from textblob import TextBlob
import numpy as np
import queue

abusive_keywords = ["abuse", "hate", "stupid", "idiot", "fool"]

def is_abusive(text):
    return [word for word in abusive_keywords if word in text.lower()]

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

result_queue = queue.Queue()

class AudioProcessor(AudioProcessorBase):
    def recv(self, frame):
        audio_data = np.frombuffer(frame.to_ndarray(), dtype=np.int16)
        result_queue.put(audio_data)
        return frame

st.title("🎙️ Live Voice Abuse & Sentiment Detector")

ctx = webrtc_streamer(
    key="speech",
    mode="sendonly",
    audio_receiver_size=1024,
    client_settings={"mediaStreamConstraints": {"audio": True, "video": False}},
    audio_processor_factory=AudioProcessor,
)

if st.button("Analyze Live Audio"):
    recognizer = sr.Recognizer()
    audio_frames = []

    while not result_queue.empty():
        audio_frames.append(result_queue.get())

    if audio_frames:
        audio_bytes = np.concatenate(audio_frames).tobytes()
        audio = sr.AudioData(audio_bytes, sample_rate=48000, sample_width=2)

        try:
            text = recognizer.recognize_google(audio)
            st.write("🗣️ Transcribed Text:", text)

            abusive = is_abusive(text)
            sentiment = get_sentiment(text)

            if abusive:
                st.error(f"⚠️ Abusive language detected: {', '.join(abusive)}")
            elif sentiment < -0.5:
                st.warning("⚠️ Negative sentiment detected.")
            else:
                st.success("✅ Normal speech.")
        except Exception as e:
            st.warning("Speech could not be recognized.")
