import streamlit as st
from gtts import gTTS
import os

# Function to generate speech
def generate_speech(text, language):
    tts = gTTS(text=text, lang=language)
    filename = "speech.mp3"
    tts.save(filename)
    return filename

# Streamlit UI
st.title("Text to Speech")

# Text input
text = st.text_area("Enter text:")

# Language selection
language = st.selectbox("Select Language", ['en', 'es', 'fr', 'de', 'it'])

# Generate and play speech
if st.button("Generate Speech"):
    if text:
        filename = generate_speech(text, language)
        st.audio(filename, format="audio/mp3")
        st.success("Speech generated successfully!")

# Download the generated speech
if st.button("Download Voice"):
    if text:
        filename = generate_speech(text, language)
        with open(filename, "rb") as file:
            btn = st.download_button(
                label="Download MP3",
                data=file,
                file_name=filename,
                mime="audio/mpeg"
            )
        st.success("Downloaded successfully!")
