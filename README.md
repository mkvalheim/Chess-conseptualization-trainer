# Chess Conceptualization Trainer

A collection of tools to help chess players improve their visualization and conceptualization skills.

## Features

### PGN to Audio Converter
- Converts PGN files to MP3 audio files
- Speaks chess moves in natural language (e.g., "Pawn to e4", "Knight takes f3")
- Customizable pause lengths between moves
- Announces checks, checkmates, and game results
- Perfect for blindfold chess training

### Square Color Trainer
- Interactive game to improve board visualization
- Challenges players to identify the color of chess squares
- Tracks score and completion time
- Includes keyboard shortcuts for faster play (W/Left Arrow for White, B/Right Arrow for Black)
- Game ends after 25 correct answers or one wrong answer

## Installation

1. Clone this repository
2. Install the required packages:
```
pip install -r requirements.txt
```

## Usage

### Running the Application Locally

Start the Streamlit app:

```
streamlit run app.py
```

### Using the PGN to Audio Converter

You can either:
1. Use the web interface through the Streamlit app
2. Call the module directly in your code:

```python
from modules.pgn_to_audio import pgn_to_mp3

pgn_to_mp3("your_game.pgn", 
    pause_length_1=2.0,  # 2.0 second pause after move number
    pause_length_2=3.0,  # 3.0 second pause between white and black moves
    pause_length_3=3.0   # 3.0 second pause between turns
)
```

### Using the Square Color Trainer

Access the trainer through the Streamlit app and:
1. Click "New Game" to start
2. Identify if each displayed square (e.g., "e4") is white or black
3. Use mouse clicks or keyboard shortcuts (W/Left Arrow for White, B/Right Arrow for Black)
4. Try to complete 25 correct identifications as quickly as possible

## Requirements

- Python 3.6+
- streamlit
- python-chess
- gTTS (Google Text-to-Speech)
- moviepy
- python-dotenv 

## Live Demo

A live version of this application is deployed on Streamlit and available at:
[Chess Conceptualization Trainer](https://chess-conceptualization-trainer.streamlit.app/)

## Development

This project was created as part of my own chess training, following courses on [Don't Move Until You See It](https://dontmoveuntilyousee.it/).

## License

This project is licensed under the terms of the MIT license. 