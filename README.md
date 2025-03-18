# PGN to Audio

Convert chess games in PGN format to audio for blind chess players or for learning chess while on the go.

## Features

- Converts PGN files to MP3 audio files
- Speaks chess moves in natural language (e.g., "Pawn to e4", "Knight takes f3")
- Customizable pause lengths between moves
- Announces checks, checkmates, and game results

## Installation

1. Clone this repository
2. Install the required packages:
```
pip install -r requirements.txt
```

## Usage

Place your PGN file in the project directory and run:

```
python pgn_to_audio.py
```

By default, it will look for a file called `game.pgn`. To use a different file or customize pause lengths:

```python
pgn_to_mp3("your_game.pgn", 
    pause_length_1=0.5,  # 0.5 second pause after move number
    pause_length_2=1.5,  # 1.5 second pause between white and black moves
    pause_length_3=2.0   # 2.0 second pause between turns
)
```

## Requirements

- Python 3.6+
- python-chess
- gTTS (Google Text-to-Speech)
- moviepy
- python-dotenv 