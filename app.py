import streamlit as st

# Define abusive keywords (for demo purposes)
abusive_keywords = ["abuse", "hate", "stupid", "idiot", "fool"]

def is_abusive(text):
    found = [word for word in abusive_keywords if word in text.lower()]
    return found

# Streamlit App UI
st.title("Abuse Detector 🔍")

user_input = st.text_area("Enter your message:")

if st.button("Check"):
    result = is_abusive(user_input)
    if result:
        st.error(f"⚠️ Abusive content detected: {', '.join(result)}")
    else:
        st.success("✅ No abusive content found.")
