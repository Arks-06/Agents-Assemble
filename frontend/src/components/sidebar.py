import streamlit as st
from config import settings

def render_sidebar():
    """Renders the left control panel."""
    with st.sidebar:
        st.title("🛡️ Agents Assemble")

        auth_token = st.text_input("Admin JWT Token", type="password", help="Paste token from FastAPI Swagger")
        if auth_token:
            st.session_state.access_token = auth_token

        st.markdown("---")
        
        st.markdown("### Configuration")
        agent_type = st.selectbox(
            "Select Agent Pipeline", 
            ["Deep Research Agent", "Summarization Agent", "Code Review Agent"]
        )
        
        st.markdown("---")
        st.caption(f"🔗 Connected to: `{settings.BACKEND_URL}`")
        
        # Add a clear memory button
        if st.button("Clear Chat Memory", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
            
        return agent_type