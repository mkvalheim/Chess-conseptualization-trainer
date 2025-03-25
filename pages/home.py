import sys
import os
import streamlit as st

st.set_page_config(
    page_title="Chess Conceptualization Trainer",
    page_icon="♟️"
    )

# Add modules directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))




st.title("Chess Conceptualization Trainer")


st.write("Improve your chess visualization skills with audio-based training tools")

st.markdown("""
## Welcome to the Chess Conceptualization Trainer!

This site contains various tools to help you improve your chess skills. I have made these tools for myself as a part of my own training with chess conceptualization while following the courses on [Dont move untill you see it](https://dontmoveuntilyousee.it).

### Available Tools:""")

st.page_link("pages/pgn_to_audio.py", label="PGN to Audio Converter", icon=":material/graphic_eq:")
st.page_link("pages/square_color_trainer.py", label="Square Color Trainer", icon=":material/invert_colors:")

st.markdown("""
More tools coming soon!

### How to Use:

Select a tool from the sidebar to get started.

---
*Developed for chess enthusiasts looking to enhance their mental game*
""")