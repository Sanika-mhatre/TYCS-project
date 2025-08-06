import streamlit as st
import base64

# Set page config (only runs once here)
st.set_page_config(
    page_title="Academic Research Analyzer",
    page_icon="📚",
    layout="wide"
)

# Inject custom CSS (if style.css exists)
def load_css(file_path):
    with open(file_path, "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

# Optional: Background image (replace with your bg.jpg)
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{b64}");
            background-size: cover;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# Load styling
load_css("assets/style.css")
# set_background("assets/bg.jpg")  # Optional background image

# Main Header
st.markdown("<h1 style='text-align: center; color: #4A7EBB;'>📚 Academic Research Paper Analyzer Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload, analyze, and evaluate your research paper instantly.</p>", unsafe_allow_html=True)

