import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        /* 1. Force the entire page background to be the gradient */
        .stApp {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
            background-attachment: fixed;
        }

        /* 2. Ensure the main content block is transparent so the gradient shows through */
        .stApp [data-testid="stMainBlockContainer"] {
            background-color: transparent !important;
        }

        /* 3. Stylish Chat Bubbles */
        .stChatMessage {
            background-color: rgba(255, 255, 255, 0.08) !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(5px);
        }

        /* 4. Glowing Buttons */
        div.stButton > button {
            background: linear-gradient(to right, #6a11cb, #2575fc) !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            transition: 0.3s !important;
        }
        div.stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px #2575fc !important;
        }
        </style>
    """, unsafe_allow_html=True)