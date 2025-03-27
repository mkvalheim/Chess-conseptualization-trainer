import chess.pgn
import re
import os
import time
import requests
import streamlit as st
import io
from elevenlabs import ElevenLabs
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips, AudioClip
import tempfile






def create_silence(duration):
    """Create a silent audio clip of specified duration in seconds"""
    return AudioClip(lambda t: 0, duration=duration)

def text_to_audio(text):
    """Convert text to audio using ElevenLabs and return the audio clip"""
    try:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_file.close()
        
        # Get audio data from ElevenLabs
        audio_gen = client.text_to_speech.convert(
            text=text,
            voice_id="21m00Tcm4TlvDq8ikWAM",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        
        # Convert generator to bytes
        audio_bytes = b''
        for chunk in audio_gen:
            audio_bytes += chunk
        
        # Save the audio data to the temporary file
        with open(temp_file.name, "wb") as f:
            f.write(audio_bytes)
        
        # Load the audio clip from the file
        audio_clip = AudioFileClip(temp_file.name)
        
        # Delete the temporary file
        os.unlink(temp_file.name)
        
        return audio_clip
    except Exception as e:
        print(f"Error in text_to_audio: {str(e)}")
        # Return a silent clip as fallback
        return create_silence(1)

def parse_turn(turn):
    turn_parts = turn.split(" ")
    print(f'Turn parts: {turn_parts}')
    move_number = turn_parts[0]
    white_move = turn_parts[1]
    black_move = turn_parts[2] if len(turn_parts) > 2 else None
    result = re.search(r'\d+-\d+|[1/2]-[1/2]', turn)
    result = result.group() if result else None
    return move_number, white_move, black_move, result

def turn_to_audio(turn, pause_length_1=1, pause_length_2=2, pause_length_3=3):
    print(f'Processing turn: {turn}')
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

        print(f'Processing move: {move}')
        
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

        # Append the move text to a file
        with open("move_text.txt", "a") as f:
            f.write(move_text + "\n")

        # Add the move audio
        audio_clips.append(text_to_audio(move_text))
        
        # Add pause_2 between moves
        if i < len(moves) - 1 and moves[i + 1]:
            audio_clips.append(create_silence(pause_length_2))

        if '#' in move:
            print("Found checkmate, breaking")  
            break
    
    # Add pause_3 at the end of the turn
    audio_clips.append(create_silence(pause_length_3))
    
    if result:
        result_text = result_map_checkmate[result] if '#' in str(moves) else result_map[result]
        audio_clips.append(text_to_audio(result_text))

    # Concatenate all clips
    return concatenate_audioclips(audio_clips)

d

def turn_to_audiobytes(turn, pause_length_1=2, pause_length_2=3, pause_length_3=3):
    print(f'Processing turn: {turn}')
    move_number, white_move, black_move, result = parse_turn(turn)

    # Initialize elevenlabs client
    client = ElevenLabs(api_key=st.secrets["eleven_labs_api_key"])

    # Insert SSML tags for pauses between moves
    white_move_ssml = f"""
    {move_number}
    <break time="{pause_length_1}s"/>
    {white_move}
    """

    black_move_ssml = f"""
    {black_move}
    <break time="{pause_length_3}s"/>
    {result if result else ""}
    """

    white_move_audio_bytes = text_to_audio_bytes(white_move_ssml)
    black_move_audio_bytes = text_to_audio_bytes(black_move_ssml)

    return black_move_audio_bytes, white_move_audio_bytes
    


def pgn_to_mp3(pgn_file, pause_length_1=2, pause_length_2=3, pause_length_3=3):
    
    print("Starting...")
    t = time.time()

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
            turn_audio = turn_to_audio(turn, pause_length_1, pause_length_2, pause_length_3)
            audio_clips.append(turn_audio)

        # Concatenate all turns and write to file
        final_audio = concatenate_audioclips(audio_clips)
        
        # Fix for 'CompositeAudioClip' object has no attribute 'fps'
        if not hasattr(final_audio, 'fps') and audio_clips:
            # Set fps based on the first clip or use default 44100
            for clip in audio_clips:
                if hasattr(clip, 'fps') and clip.fps:
                    final_audio.fps = clip.fps
                    break
            if not hasattr(final_audio, 'fps') or not final_audio.fps:
                final_audio.fps = 44100  # Standard audio sample rate
                
        final_audio.write_audiofile("game.mp3")
        
        print("Audio file created successfully.")
        print("Done in " + str(time.time() - t) + " seconds")

        return True
    except Exception as e:
        import traceback
        print(f"Error in pgn_to_mp3: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    # Pause lengths are in seconds
    pgn_to_mp3("game.pgn", 
        pause_length_1=0.5,    # 0.5 seconds
        pause_length_2=1.5,    # 1.5 seconds
        pause_length_3=2.0     # 2 seconds
    )

