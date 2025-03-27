import streamlit as st
import os

# Set page title
st.title("Chess Diagonals Trainer")

with open(os.path.join(os.path.dirname(__file__), 'diagonals_trainer.html'), 'r') as f: 
    html_content = f.read()

# Display the HTML content with adjusted height
st.components.v1.html(html_content, height=600)
