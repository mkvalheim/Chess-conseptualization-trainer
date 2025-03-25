import streamlit as st
import os

# Set page title
st.title("Chess Square Color Trainer")

# Read the HTML file
with open(os.path.join(os.path.dirname(__file__), 'square_color_trainer.html'), 'r') as f:
    html_content = f.read()

# Display the HTML content with adjusted height
st.components.v1.html(html_content, height=900)
