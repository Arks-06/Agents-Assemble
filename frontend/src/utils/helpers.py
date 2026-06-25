import streamlit as st

def initialize_session_state():
    """Ensures chat history survives page refreshes."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def add_message(role: str, content: str):
    """Helper to append messages to the UI state."""
    st.session_state.messages.append({"role": role, "content": content})