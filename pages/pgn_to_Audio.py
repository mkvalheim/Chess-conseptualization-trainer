import streamlit as st
import os
import time
import sys

# Add error handling for dependency imports
try:
    import chess.pgn
    import re
    import tempfile
    from gtts import gTTS
    from moviepy.audio import AudioClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    from moviepy.audio.AudioClip import concatenate_audioclips
except ImportError as e:
    st.error(f"""
    ### Missing Dependencies
    
    The following dependency could not be imported: `{e.name}`
    
    Please make sure all required packages are installed by running:
    ```
    pip install -r requirements.txt
    ```
    
    Required packages:
    - streamlit
    - chess
    - gtts
    - moviepy
    - python-dotenv
    """)
    st.stop()

# Add the working directory to the path so we can import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from modules.pgn_to_audio import pgn_to_mp3
except ImportError:
    st.error("""
    ### Module Import Error
    
    Could not import the pgn_to_audio module. Please ensure the modules directory exists and contains the required file.
    """)
    st.stop()

def render_pgn_to_audio():
    st.title("PGN to Audio Converter")
    st.write("Convert chess games to audio narration for blindfold training")

    # Create dropdown for audio generation settings
    audio_settings = st.expander("Settings", icon=":material/settings:")

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

    # Set up a temp directory relative to the root of the app
    temp_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp"))
    os.makedirs(temp_dir, exist_ok=True)
    temp_pgn_path = os.path.join(temp_dir, "temp.pgn")
    output_mp3_path = os.path.join(temp_dir, "game.mp3")

    with tab1:
        st.write("Upload a PGN file")
        uploaded_file = st.file_uploader("Choose a PGN file", type=['pgn'], key="file_uploader")
        if uploaded_file is not None:
            with open(temp_pgn_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            pgn_source = temp_pgn_path

    with tab2:
        st.write("Paste your PGN directly")
        pasted_pgn = st.text_area("Paste PGN here", height=200)
        if pasted_pgn:
            with open(temp_pgn_path, "w") as f:
                f.write(pasted_pgn)
            pgn_source = temp_pgn_path


    # Convert button (only show if we have a PGN source)
    if 'pgn_source' in locals():
        if st.button("Convert to Audio"):
            with st.spinner("Converting PGN to audio..."):
                try:
                    # Modified to use absolute path for output
                    result = pgn_to_mp3(pgn_source, pause_length_1, pause_length_2, pause_length_3)
                    if result:
                        st.success("Conversion complete!")
                        
                        # Audio player
                        if os.path.exists(output_mp3_path):
                            st.audio(output_mp3_path)
                        else:
                            st.error("Audio file was not created successfully")
                    else:
                        st.error("Conversion failed")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        
        # Cleanup
        if os.path.exists(temp_pgn_path):
            try:
                os.remove(temp_pgn_path)
            except:
                pass

    # Add some helpful information
    with st.expander("How to use"):
        st.write("""
        Choose one of two methods to input your chess game:
        
        1. **Upload PGN**: Upload a PGN file from your computer
        2. **Paste PGN**: Copy and paste the PGN directly into the text area
        
        Then:
        1. Click the 'Convert to Audio' button
        2. Wait for the conversion to complete
        3. Use the audio player to listen to the game
        """) 
    st.markdown("""
    **Tips for Effective Training:**

    - Practice regularly with short sessions
    - Start with simple positions and gradually increase difficulty
    - Visualize the board after each move
    - Use the pause settings to give yourself time to visualize
    """)
render_pgn_to_audio()

# When this file is run directly, set the page config and render
if __name__ == "__main__":
    st.set_page_config(
        page_title="PGN to Audio Converter",
        page_icon="♟️"
    )
    
    # Add navigation back to home
    if st.sidebar.button("← Back to Home"):
        st.switch_page("app.py")
        
    render_pgn_to_audio() 