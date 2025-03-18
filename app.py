import streamlit as st
import os
from pgn_to_audio import pgn_to_mp3
import time
from chess_com import get_pgn_from_chess_com

st.set_page_config(page_title="Chess PGN to Audio", page_icon="♟️")

st.title("Chess PGN to Audio Converter")
st.write("Convert chess games to audio narration")

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
                pgn_to_mp3(pgn_source)
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
    3. **Chess.com URL**: Enter a link to a game on Chess.com
    
    Then:
    1. Click the 'Convert to Audio' button
    2. Wait for the conversion to complete
    3. Use the audio player to listen to the game
    """) 