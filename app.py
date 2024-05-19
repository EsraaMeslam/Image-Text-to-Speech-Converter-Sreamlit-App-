import streamlit as st
from PIL import Image
import pytesseract
from gtts import gTTS
import numpy as np
import base64

pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe" # read pytesseract file


st.title("Image Text to Speech Converter App")
st.markdown("<h6 style='text-align: center'>Welcome to the App! I hope you'll enjoy your time here.💗💗</h1>", unsafe_allow_html=True)


def generate_audio(text):
    tts = gTTS(text)
    tts.save('audio.mp3')
    return 'audio.mp3'


uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)

    st.image(img)

    # Convert to grayscale
    gray = img.convert('L')

    try:
        text = pytesseract.image_to_string(gray)
        if text.strip() == '':
            raise ValueError("No text detected in the image so please choose an image that contains text and try again. 💗💗")
    except Exception as e:
        st.error("OPPS: {}".format(e))
    else:
        st.markdown("<h2 style='text-align: center'>💬Extracted Text...</h2>", unsafe_allow_html=True)
        st.write(text)

        st.markdown("<h2 style='text-align: center'>🔊Generating audio...</h2>", unsafe_allow_html=True)

        # Generate audio
        audio_file = generate_audio(text)

        # Display audio file
        st.audio(audio_file, format='audio/mp3', start_time=0)
        st.success("Audio generated successfully!")

        download_audio = st.checkbox("Do you want to download the audio?")

        if download_audio:
            with open(audio_file, 'rb') as f:
                audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            href = f'<a href="data:audio/mp3;base64,{b64}" download="generated_audio.mp3">Click here to download audio</a>'
            st.markdown(href, unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: center;'>Thank you for using the App!! I hope you have a nice day.🤩</h3>", unsafe_allow_html=True)
