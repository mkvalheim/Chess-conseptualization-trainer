import os
import streamlit as st
from elevenlabs import ElevenLabs

api_key = st.secrets["eleven_labs_api_key"]
client = ElevenLabs(api_key=st.secrets["eleven_labs_api_key"])

def text_to_audio_bytes(text):
    audio_gen = client.text_to_speech.convert(
        text=text,
        voice_id="21m00Tcm4TlvDq8ikWAM",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    audio_bytes = b''
    for chunk in audio_gen:
        audio_bytes += chunk
    return audio_bytes