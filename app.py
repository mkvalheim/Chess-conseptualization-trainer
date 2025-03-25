import streamlit as st
import sys
import os

st.set_page_config(
    page_title="Chess Conceptualization Trainer",
    page_icon="♟️"
)

# Add modules directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



pages = {
    "Main": [
        st.Page("pages/home.py", title="Home"),
    ],
    "Tools": [
        st.Page("pages/pgn_to_Audio.py", title="PGN to Audio Converter"),
        st.Page("pages/square_color_trainer.py", title="Square Color Trainer"),
    ],
}

pg = st.navigation(pages)
pg.run()

st.title("Chess Conceptualization Trainer")
st.write("Improve your chess visualization skills with audio-based training tools")