import streamlit as st
from textblob import TextBlob
from twilio.rest import Client

# Abusive words list
abusive_keywords = ["abuse", "hate", "stupid", "idiot", "fool"]

def is_abusive(text):
    return [word for word in abusive_keywords if word in text.lower()]

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # -1 to 1

def send_sms_alert(message):
    # Replace with your Twilio credentials
    account_sid = 'YOUR_TWILIO_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_='+1XXXXXXXXXX',  # Twilio phone number
        to='+91XXXXXXXXXX'    # Your verified phone
    )

# UI
st.title("Voice/Text Abuse & Sentiment Monitor 🔍")
user_input = st.text_area("Enter your message or paste transcribed voice:")

if st.button("Analyze"):
    if user_input:
        abusive = is_abusive(user_input)
        sentiment = get_sentiment(user_input)

        if abusive:
            st.error(f"⚠️ Abusive content detected: {', '.join(abusive)}")
            send_sms_alert(f"Abuse Alert 🚨: {user_input}")
        elif sentiment < -0.5:
            st.warning("⚠️ Negative tone detected.")
            send_sms_alert(f"Tone Alert 🚨: Negative message - {user_input}")
        else:
            st.success("✅ No abuse or negative tone detected.")
