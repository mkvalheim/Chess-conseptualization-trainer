import streamlit as st

pages = {
    "": [
        st.Page("pages/home.py", title="Home"),
    ],
    "Tools": [
        st.Page("pages/pgn_to_audio.py", title="PGN to Audio Converter"),
        st.Page("pages/square_color_trainer.py", title="Square Color Trainer"),
    ],
}
pg = st.navigation(pages)
pg.run()