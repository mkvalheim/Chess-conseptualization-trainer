import streamlit as st

st.set_page_config(
    page_title="Chess Conceptualization Trainer",
    page_icon="♟️",
    layout="wide"
)

st.title("Chess Conceptualization Trainer")
st.write("Improve your chess visualization skills with audio-based training tools")

st.markdown("""
## Welcome to the Chess Conceptualization Trainer!

This application helps you improve your chess visualization and blindfold chess skills.

### Available Tools:

- **PGN to Audio Converter**: Convert chess games in PGN format to audio narration for blindfold training
- More tools coming soon!

### How to Use:

Select a tool from the sidebar to get started.

### Tips for Effective Training:

- Practice regularly with short sessions
- Start with simple positions and gradually increase difficulty
- Visualize the board after each move
- Use the pause settings to give yourself time to visualize

---
*Developed for chess enthusiasts looking to enhance their mental game*
""")

# Add footer with version information
st.sidebar.markdown("---")
st.sidebar.markdown("v1.0.0") 