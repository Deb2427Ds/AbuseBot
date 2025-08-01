import streamlit as st
import speech_recognition as sr
from textblob import TextBlob
from io import BytesIO
from pydub import AudioSegment

# Abusive words
abusive_keywords = ["abuse", "hate", "stupid", "idiot", "fool"]

def is_abusive(text):
    return [word for word in abusive_keywords if word in text.lower()]

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError:
            return "API unavailable."

# UI
st.title("🎤 Voice/Text Abuse & Sentiment Monitor")

input_mode = st.radio("Choose input mode:", ("Text", "Voice"))

if input_mode == "Text":
    user_input = st.text_area("Enter message:")
else:
    uploaded_audio = st.file_uploader("Upload WAV audio file", type=["wav"])
    user_input = ""
    if uploaded_audio:
        # Convert to audio segment and re-save in memory if needed
        audio_bytes = BytesIO(uploaded_audio.read())
        user_input = transcribe_audio(audio_bytes)
        st.write("Transcribed Text:")
        st.write(user_input)

if st.button("Analyze"):
    if user_input.strip():
        abusive = is_abusive(user_input)
        sentiment = get_sentiment(user_input)

        if abusive:
            st.error(f"⚠️ Abusive content: {', '.join(abusive)}")
            st.toast("🚨 Abusive language detected.")
        elif sentiment < -0.5:
            st.warning("⚠️ Negative tone detected.")
            st.toast("🚨 Negative sentiment alert.")
        else:
            st.success("✅ Clean message.")
            st.toast("✅ Message is clean.")
    else:
        st.info("Please provide a message or audio input.")
