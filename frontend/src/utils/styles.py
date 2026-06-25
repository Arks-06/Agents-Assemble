import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        /* Modern Gradient Background */
        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
        }
        /* Stylish Chat Bubbles */
        .stChatMessage {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        /* Glowing Buttons */
        div.stButton > button {
            background: linear-gradient(to right, #6a11cb, #2575fc);
            color: white;
            border: none;
            border-radius: 20px;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px #2575fc;
        }
        </style>
    """, unsafe_allow_html=True)