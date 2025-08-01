import streamlit as st
from textblob import TextBlob
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import numpy as np

# List of abusive keywords
abusive_keywords = ["abuse", "hate", "stupid", "idiot", "fool"]

def is_abusive(text):
    return [word for word in abusive_keywords if word in text.lower()]

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Range: -1 (neg) to 1 (pos)

st.title("🎙️ Real-time Audio Abuse & Sentiment Monitor")

# Voice input section
st.header("🎧 Voice Input")
recognizer = sr.Recognizer()

def transcribe_voice():
    with sr.Microphone() as source:
        st.info("Listening... please speak clearly.")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            st.success(f"Transcribed Text: {text}")
            return text
        except sr.WaitTimeoutError:
            st.error("⏱️ Timeout: No speech detected.")
        except sr.UnknownValueError:
            st.error("🤷 Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"❌ API Error: {e}")
    return ""

if st.button("🎙️ Start Voice Analysis"):
    user_input = transcribe_voice()
    if user_input:
        abusive = is_abusive(user_input)
        sentiment = get_sentiment(user_input)

        if abusive:
            st.error(f"🚨 Abusive content detected: {', '.join(abusive)}")
        elif sentiment < -0.5:
            st.warning("😟 Strong Negative Sentiment Detected")
        else:
            st.success("✅ No abuse or strong negativity detected.")

# Optional: Text input
st.header("📝 Or Enter Text Manually")
text_input = st.text_area("Paste or type a message here:")
if st.button("Analyze Text"):
    if text_input:
        abusive = is_abusive(text_input)
        sentiment = get_sentiment(text_input)

        if abusive:
            st.error(f"🚨 Abusive content detected: {', '.join(abusive)}")
        elif sentiment < -0.5:
            st.warning("😟 Strong Negative Sentiment Detected")
        else:
            st.success("✅ No abuse or strong negativity detected.")
