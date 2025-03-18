import streamlit as st
import os
from pgn_to_audio import pgn_to_mp3
import time

st.set_page_config(page_title="Chess PGN to Audio", page_icon="♟️")

st.title("Chess PGN to Audio Converter")
st.write("Convert chess games to audio narration")

# Create dropdown for audio generation settings
audio_settings = st.expander("Settings")

with audio_settings:
    st.write("**Pause lengths in seconds**")
    st.write('It is recommended to use a good amount of pause between the move number and the white move, and between the white and black move, when using the audio for blindfold chess training.')
    pause_length_1 = st.number_input("Pause between move number and white move", value=2, min_value=0, max_value=10, step=1)
    pause_length_2 = st.number_input("Pause between white and black move", value=3, min_value=0, max_value=10, step=1)
    pause_length_3 = st.number_input("Pause at the end of the turn", value=3, min_value=0, max_value=10, step=1)
    # Speed settings for use with other TTS engines, such as openai. Currently using gTTS which does not support speed, to avoid API costs.
    #st.write('**Speed of the audio**')
    #speed = st.number_input("Speed", value=1.0, min_value=0.5, max_value=2.0, step=0.1)

# Create tabs for different input methods
tab1, tab2 = st.tabs(["Upload PGN", "Paste PGN"])

with tab1:
    st.write("Upload a PGN file")
    uploaded_file = st.file_uploader("Choose a PGN file", type=['pgn'], key="file_uploader")
    if uploaded_file is not None:
        with open("temp.pgn", "wb") as f:
            f.write(uploaded_file.getvalue())
        pgn_source = "temp.pgn"

with tab2:
    st.write("Paste your PGN directly")
    pasted_pgn = st.text_area("Paste PGN here", height=200)
    if pasted_pgn:
        with open("temp.pgn", "w") as f:
            f.write(pasted_pgn)
        pgn_source = "temp.pgn"


# Convert button (only show if we have a PGN source)
if 'pgn_source' in locals():
    if st.button("Convert to Audio"):
        with st.spinner("Converting PGN to audio..."):
            try:
                pgn_to_mp3(pgn_source, pause_length_1, pause_length_2, pause_length_3)
                st.success("Conversion complete!")
                
                # Audio player
                if os.path.exists("game.mp3"):
                    st.audio("game.mp3")
                else:
                    st.error("Audio file was not created successfully")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    # Cleanup
    if os.path.exists("temp.pgn"):
        os.remove("temp.pgn")

# Add some helpful information
with st.expander("How to use"):
    st.write("""
    Choose one of three methods to input your chess game:
    
    1. **Upload PGN**: Upload a PGN file from your computer
    2. **Paste PGN**: Copy and paste the PGN directly into the text area
    
    Then:
    1. Click the 'Convert to Audio' button
    2. Wait for the conversion to complete
    3. Use the audio player to listen to the game
    """) 