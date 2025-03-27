import sys
import os
import streamlit as st


# Add modules directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


st.title("Chess Conceptualization Trainer")
st.markdown("""Improve your chess visualization skills with these training tools.
         
As a part of my own chess training and following the courses on [Dont move until you see it](https://dontmoveuntilyousee.it/), 
I've developed these tools to help myself and others train chess conceptualization.

This is a work in progress and something I work on in my spare time here and there, so I'll keep adding and changing things as I go and I might also break it from time to time. Bear with me.
""")
st.divider()

st.markdown("### Available Tools")


st.page_link("site_pages/square_color_trainer.py", label="**Square Color Trainer**", icon=":material/invert_colors:")
st.markdown("*Practice identifying the color of chess squares to improve your board visualization*")

st.page_link("site_pages/diagonals_trainer.py", label="**Diagonals Trainer**", icon=":material/texture:")
st.markdown("*Practice identifying the diagonals of chess squares to improve your board visualization*")

st.page_link("site_pages/pgn_to_audio.py", label="**PGN to Audio Converter**", icon=":material/graphic_eq:")
st.markdown("*Convert your chess games from PGN format to audio narration for blindfold training*")

st.divider()
st.markdown("""

### How to Use:

1. Select a tool from the list above or from the sidebar
2. Follow the instructions for each tool
3. Practice regularly to improve your skills


---
*Developed by Magnus Kvalheim. The project is open source and available on [GitHub](https://github.com/mkvalheim/Chess-conseptualization-trainer)*
""")