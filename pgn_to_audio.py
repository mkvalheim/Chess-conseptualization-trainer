import chess.pgn
import re
import os
import time
from gtts import gTTS
from moviepy.editor import AudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import concatenate_audioclips
import tempfile


print("Starting...")
t = time.time()

# Define the maps
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
    "a": "Pawn",
    "b": "Pawn",
    "c": "Pawn",
    "d": "Pawn",
    "e": "Pawn",
    "f": "Pawn",
    "g": "Pawn",
    "h": "Pawn",
    "N": "Knight",
    "B": "Bishop",
    "R": "Rook",
    "Q": "Queen",
    "K": "King"
}

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

def pgn_to_mp3(pgn_file, pause_length_1=1, pause_length_2=2, pause_length_3=3):
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
        final_audio.write_audiofile("game.mp3")
        
        print("Audio file created successfully.")
        return True
    except Exception as e:
        print(f"Error in pgn_to_mp3: {str(e)}")
        return False

if __name__ == "__main__":
    # Pause lengths are in seconds
    pgn_to_mp3("game.pgn", 
        pause_length_1=0.5,    # 0.5 seconds
        pause_length_2=1.5,    # 1.5 seconds
        pause_length_3=2.0     # 2 seconds
    )

print("Done in " + str(time.time() - t) + " seconds")