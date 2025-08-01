import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr
from textblob import TextBlob
import tempfile
import queue
import av

st.set_page_config(page_title="🎤 Live Audio Sentiment", layout="centered")

st.title("🎤 Live Audio Sentiment Analyzer")

# Create a queue to hold audio data
audio_queue = queue.Queue()

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_buffer = []

    def recv(self, frame: av.AudioFrame):
        pcm_data = frame.to_ndarray().flatten().tobytes()
        audio_queue.put(pcm_data)
        return frame

webrtc_streamer(
    key="speech",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"video": False, "audio": True},
    async_processing=True,
)

# Combine and save audio from queue
if st.button("Analyze Speech"):
    st.info("Processing...")

    audio_data = b""
    while not audio_queue.empty():
        audio_data += audio_queue.get()

    # Save to a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_data)
        temp_audio_path = f.name

    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_audio_path) as source:
        try:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            st.subheader("📝 Transcription")
            st.write(text)

            sentiment = TextBlob(text).sentiment
            st.subheader("🔍 Sentiment")
            st.write(f"Polarity: {sentiment.polarity:.2f}")
            st.write("Sentiment:",
                     "😊 Positive" if sentiment.polarity > 0.1 else
                     "😐 Neutral" if -0.1 <= sentiment.polarity <= 0.1 else
                     "😠 Negative")

        except sr.UnknownValueError:
            st.warning("Could not understand the audio.")
        except sr.RequestError:
            st.error("Speech recognition service is unavailable.")
