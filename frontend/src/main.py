import streamlit as st
from components.auth import render_auth_page
from components.sidebar import render_sidebar
from components.chat_ui import render_chat_history, handle_async_research
from api_client import start_research_task
from utils.helpers import initialize_session_state, add_message
from utils.styles import inject_custom_css

inject_custom_css()

# Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="Agents Assemble", 
    page_icon="🤖", 
    layout="wide"
)

# Check Authentication
if "access_token" not in st.session_state or not st.session_state["access_token"]:
    render_auth_page()
    st.stop() # <-- Prevents any of the workspace code below from running!

# Setup State and UI Layout
initialize_session_state()

# logout button to the sidebar
with st.sidebar:
    if st.button("Logout", type="primary"):
        st.session_state["access_token"] = None
        st.rerun()

selected_agent = render_sidebar()

st.title(f"🔍 {selected_agent} Workspace")
st.markdown("Enter a topic below. The heavy lifting is offloaded to the background worker.")

# Render previous messages
render_chat_history()

# Handle User Input
if prompt := st.chat_input("Enter a research topic..."):
    
    # Draw user message instantly
    add_message("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Dispatch to FastAPI
    task_id = start_research_task(prompt)
    
    if task_id:
        with st.chat_message("assistant"):
            final_response = handle_async_research(task_id)
            st.markdown(final_response)
            add_message("assistant", final_response)
    else:
        st.error("🚨 Failed to dispatch task. Ensure FastAPI and Redis are running.")