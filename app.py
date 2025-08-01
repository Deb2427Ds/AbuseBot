import streamlit as st
from streamlit_webrtc import webrtc_streamer, ClientSettings, WebRtcMode
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import speech_recognition as sr
from textblob import TextBlob
import numpy as np
import queue

# Keywords to flag abusive content
abusive_keywords = ["abuse", "hate", "stupid", "idiot", "fool"]

def is_abusive(text):
    return [word for word in abusive_keywords if word in text.lower()]

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Queue to store audio frames
result_queue = queue.Queue()

class AudioProcessor(AudioProcessorBase):
    def recv(self, frame):
        audio_data = np.frombuffer(frame.to_ndarray(), dtype=np.int16)
        result_queue.put(audio_data)
        return frame

# App UI
st.title("🎙️ Live Voice Abuse & Sentiment Detector")

# Start audio stream from microphone
from streamlit_webrtc import webrtc_streamer, ClientSettings

ctx = webrtc_streamer(
    key="speech",
    mode=WebRtcMode.SENDRECV,  # this fixes the AttributeError
    client_settings=ClientSettings(
        media_stream_constraints={"audio": True, "video": False},
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        }
    ),
    audio_receiver_size=1024,
    audio_processor_factory=AudioProcessor  # ensure this class is implemented
)

class AudioProcessor:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

    def recv(self, frame):
        # You can process the audio frame here
        return frame


# Run analysis on captured audio
if st.button("Analyze Live Audio"):
    recognizer = sr.Recognizer()
    audio_frames = []

    # Collect all audio from the queue
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
            st.warning("⚠️ Speech could not be recognized. Try again.")
    else:
        st.info("No audio input was received yet. Please speak and then click Analyze.")
