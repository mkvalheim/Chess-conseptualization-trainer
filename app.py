import streamlit as st
import sys
import os

st.set_page_config(
    page_title="Chess Conceptualization Trainer",
    page_icon="♟️"
)

# Add modules directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def back_to_home():
    st.Page("pages/home.py")


pages = {
    "Main": [
        st.Page("site_pages/home.py", title="Home"),
    ],
    "Tools": [
        st.Page("site_pages/pgn_to_audio.py", title="PGN to Audio Converter"),
        st.Page("site_pages/square_color_trainer.py", title="Square Color Trainer"),
        st.Page("site_pages/diagonals_trainer.py", title="Diagonals Trainer"),
    ],
}

pg = st.navigation(pages)
pg.run()

st.divider()
if "home.py" not in str(pg._page):
    st.page_link("site_pages/home.py", label="Back to Home", icon=":material/home:")