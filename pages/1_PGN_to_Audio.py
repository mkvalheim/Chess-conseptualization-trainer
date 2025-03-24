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
    from moviepy.editor import AudioClip
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
    # Define a local version of the function if module import fails
    def create_silence(duration):
        """Create a silent audio clip of specified duration in seconds"""
        return AudioClip(lambda t: 0, duration=duration)

    def text_to_audio(text):
        """Convert text to audio using gTTS and return the audio clip"""
        tts = gTTS(text=text, slow=True, lang="en")
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            tts.save(temp_file.name)
            audio = AudioFileClip(temp_file.name)
        os.unlink(temp_file.name)
        return audio

    def pgn_to_mp3(pgn_file, pause_length_1=2, pause_length_2=3, pause_length_3=3):
        global output_mp3_path  # Access the global variable defined outside
        
        # Maps needed for conversion
        extension_map = {
            "+": "check",
            "#": "checkmate",
            "=N": "promotes to knight",
            "=B": "promotes to bishop",
            "=R": "promotes to rook",
            "=Q": "promotes to queen"
        }
        
        result_map_checkmate = {
            "0-1": "Black wins",
            "1-0": "White wins",
        }
        
        result_map = {
            "0-1": "White resigns",
            "1-0": "Black resigns",
            "1/2-1/2": "Draw"
        }
        
        piece_to_string_map = {
            "": "Pawn",
            "a": "Pawn", "b": "Pawn", "c": "Pawn", "d": "Pawn",
            "e": "Pawn", "f": "Pawn", "g": "Pawn", "h": "Pawn",
            "N": "Knight", "B": "Bishop", "R": "Rook", "Q": "Queen", "K": "King"
        }
        
        def parse_turn(turn):
            turn_parts = turn.split(" ")
            move_number = turn_parts[0]
            white_move = turn_parts[1] if len(turn_parts) > 1 else None
            black_move = turn_parts[2] if len(turn_parts) > 2 else None
            result = re.search(r'\d+-\d+|[1/2]-[1/2]', turn)
            result = result.group() if result else None
            return move_number, white_move, black_move, result
        
        def turn_to_audio(turn):
            move_number, white_move, black_move, result = parse_turn(turn)
            
            # Initialize the audio clips for this turn
            audio_clips = []
            
            # Add move number with pause_1
            audio_clips.append(text_to_audio(move_number))
            audio_clips.append(create_silence(pause_length_1))
            
            moves = [white_move, black_move]
            for i, move in enumerate(moves):
                if not move:
                    continue
                
                piece = re.search(r'\A[NBRQK]|\A[a-h]', move)
                extension = re.search(r'[+#]|=[NBRQ]', move)
                
                move_text = ""
                if move == "O-O-O":
                    move_text = "Queen side castle"
                    if extension:
                        move_text += " " + extension.group()
                elif move == "O-O":
                    move_text = "King side castle"
                    if extension:
                        move_text += " " + extension.group()
                else:
                    action = "takes" if "x" in move else "to"
                    piece_name = piece_to_string_map[piece.group() if piece else ""]
                    target_square = re.search(r'[a-h][1-8]', move)
                    move_text = f"{piece_name} {action} {target_square.group() if target_square else ''}"
                    if extension:
                        move_text += f", {extension_map[extension.group() if extension else '']}"
                
                # Add the move audio
                audio_clips.append(text_to_audio(move_text))
                
                # Add pause_2 between moves
                if i < len(moves) - 1 and moves[i + 1]:
                    audio_clips.append(create_silence(pause_length_2))
                
                if '#' in move:
                    break
            
            # Add pause_3 at the end of the turn
            audio_clips.append(create_silence(pause_length_3))
            
            if result:
                result_text = result_map_checkmate[result] if '#' in str(moves) else result_map[result]
                audio_clips.append(text_to_audio(result_text))
            
            # Concatenate all clips
            return concatenate_audioclips(audio_clips)
        
        try:
            with open(pgn_file, "r") as pgn:
                game = chess.pgn.read_game(pgn)
                game_moves = game.mainline_moves()
            
            moves_string = str(game_moves) + " " + str(game.headers["Result"])
            pattern = r'(?=\s\d+[.]\s)'
            turns = [turn.strip() for turn in re.split(pattern, moves_string)]
            
            # Initialize the audio clips
            audio_clips = []
            
            # Process each turn
            for turn in turns:
                if not turn:  # Skip empty turns
                    continue
                turn_audio = turn_to_audio(turn)
                audio_clips.append(turn_audio)
            
            # Concatenate all turns and write to file
            final_audio = concatenate_audioclips(audio_clips)
            final_audio.write_audiofile(output_mp3_path)
            
            return True
        except Exception as e:
            st.error(f"Error in pgn_to_mp3: {str(e)}")
            return False

st.set_page_config(page_title="PGN to Audio Converter", page_icon="♟️")

st.title("PGN to Audio Converter")
st.write("Convert chess games to audio narration for blindfold training")

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