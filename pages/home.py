import sys
import os
import streamlit as st


# Add modules directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


st.title("Chess Conceptualization Trainer")
st.markdown("""Improve your chess visualization skills with these training tools.
         
As a part of my own chess training and following the courses on [Dont move until you see it](https://dontmoveuntilyousee.it/), 
I've developed these tools to help myself and others train chess conceptualization.
""")
box = st.container(border=True)

with box:
    st.markdown("""
    ### Available Tools:
    """)

    st.page_link("pages/pgn_to_Audio.py", label="PGN to Audio Converter", icon=":material/graphic_eq:")
    st.markdown("*Convert your chess games from PGN format to audio narration for blindfold training*")

    st.page_link("pages/square_color_trainer.py", label="Square Color Trainer", icon=":material/invert_colors:")
    st.markdown("*Practice identifying the color of chess squares to improve your board visualization*")

st.markdown("""

### How to Use:

1. Select a tool from the sidebar
2. Follow the instructions for each tool
3. Practice regularly to improve your skills

### Tips for Effective Training:

- Start with simple positions and gradually increase difficulty
- Practice in short, focused sessions
- Use the audio features to reinforce your visualization
- Track your progress over time

---
*Developed for chess enthusiasts looking to enhance their mental game*
""")