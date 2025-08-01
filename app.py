import streamlit as st
from textblob import TextBlob

# Abusive words list
abusive_keywords = ["abuse", "hate", "stupid", "idiot", "fool"]

def is_abusive(text):
    return [word for word in abusive_keywords if word in text.lower()]

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # range from -1 (very negative) to +1 (very positive)

# UI
st.title("Voice/Text Abuse & Sentiment Monitor 🔍")
user_input = st.text_area("Enter your message or paste transcribed voice:")

if st.button("Analyze"):
    if user_input.strip():
        abusive = is_abusive(user_input)
        sentiment = get_sentiment(user_input)

        if abusive:
            st.error(f"⚠️ Abusive content detected: {', '.join(abusive)}")
            st.toast("🚨 Abusive content alert sent to system monitor.")
        elif sentiment < -0.5:
            st.warning("⚠️ Negative tone detected.")
            st.toast("🚨 Negative tone alert triggered.")
        else:
            st.success("✅ No abuse or negative tone detected.")
            st.toast("✅ Message is clean.")
    else:
        st.info("Please enter a message to analyze.")
