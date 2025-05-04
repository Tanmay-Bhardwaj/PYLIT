import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr

# Page Configuration
st.set_page_config(
    page_title="Voice Translate",
    page_icon="🎙️",
)

st.title("Voice Translate")

# Custom Background Style
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(at bottom right, #E5A82F 0, #E5A82F 8.75px, #E5A82F33 8.75px, #E5A82F33 17.5px, #E5A82FBF 17.5px, #E5A82FBF 26.25px, #E5A82F40 26.25px, #E5A82F40 35px, #E5A82F4D 35px, #E5A82F4D 43.75px, #E5A82FBF 43.75px, #E5A82FBF 52.5px, #E5A82F33 52.5px, #E5A82F33 61.25px, transparent 61.25px, transparent 70px), radial-gradient(at top left, transparent 0, transparent 8.75px, #E5A82F33 8.75px, #E5A82F33 17.5px, #E5A82FBF 17.5px, #E5A82FBF 26.25px, #E5A82F4D 26.25px, #E5A82F4D 35px, #E5A82F40 35px, #E5A82F40 43.75px, #E5A82FBF 43.75px, #E5A82FBF 52.5px, #E5A82F33 52.5px, #E5A82F33 61.25px, #E5A82F 61.25px, #E5A82F 70px, transparent 70px, transparent 175px);
    background-blend-mode: multiply;
    background-size: 70px 70px, 70px 70px;
    background-color: #B2A461;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Initialize session state for recording and text storage
if "recording" not in st.session_state:
    st.session_state.recording = False
if "text" not in st.session_state:
    st.session_state.text = ""

# Function to start recording
def start_recording():
    st.session_state.recording = True

# Function to stop recording
def stop_recording():
    st.session_state.recording = False

# UI Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Start Recording 🎙️", key="start"):
        start_recording()
with col2:
    if st.session_state.recording and st.button("Stop Recording ⏹️", key="stop"):
        stop_recording()

# Continuous speech recording
if st.session_state.recording:
    st.write("Recording... Press 'Stop Recording' to finish.")
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            st.info("Listening... (Press 'Stop Recording' to stop)")
            audio = recognizer.listen(source, timeout=2100, phrase_time_limit=35)
            text_chunk = recognizer.recognize_google(audio)
            st.session_state.text += " " + text_chunk  # Append to existing text
        except sr.WaitTimeoutError:
            st.warning("Listening timed out. Waiting for input...")
        except sr.UnknownValueError:
            st.warning("Could not understand audio. Please speak again.")
        except Exception as e:
            st.error(f"Error occurred: {e}")

# Process and display after recording stops
if not st.session_state.recording and st.session_state.text:
    st.success("Recording stopped.")
    st.text_area(label="Recorded Text:", value=st.session_state.text.strip(), height=100)

    # Translations
    translated_hi = GoogleTranslator(source='auto', target='hi').translate(st.session_state.text)
    translated_mr = GoogleTranslator(source='auto', target='mr').translate(st.session_state.text)
    translated_en = GoogleTranslator(source='auto', target='en').translate(st.session_state.text)

    st.text_area(label="Hindi:", value=translated_hi, height=100)
    st.text_area(label="Marathi:", value=translated_mr, height=100)
    st.text_area(label="English:", value=translated_en, height=100)
