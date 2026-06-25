import time
import streamlit as st
from api_client import fetch_task_status

def render_chat_history():
    """Loops through session state and draws the chat."""
    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_async_research(task_id: str) -> str:
    """
    Polls the backend, renders dynamic status updates, 
    and returns a polished markdown result.
    """
    attempt = 0
    with st.spinner("Agent is actively researching..."):
        
        while True:
            # current status
            status_data = fetch_task_status(task_id)
            attempt += 1
            
            # Safety net if the API goes completely offline
            if not status_data:
                return "🚨 **Error:** Lost connection to the backend API."

            current_status = status_data.get("status")

            # Celery finished the job!
            if current_status == "SUCCESS":
                st.toast("Research Complete!", icon="✅")
                
                celery_result = status_data.get("result", {})
                actual_data = celery_result.get("data", {}) 
                
                if isinstance(actual_data, dict):
                    topic = actual_data.get("topic", "Unknown Topic")
                    summary = actual_data.get("summary", "No summary provided.")
                    takeaways = actual_data.get("key_takeaways", [])
                    
                    # Error resiliency: Checks for fallback partial success
                    if "Format boundary reached" in str(takeaways):
                        return f"⚠️ **Partial Results Only:**\n\n{summary}"
                    
                    formatted_response = f"### 🔬 Research: {topic}\n\n**Summary:**\n{summary}\n\n"
                    
                    if takeaways:
                        formatted_response += "**Key Takeaways:**\n"
                        for point in takeaways:
                            formatted_response += f"- {point}\n"
                    else:
                        formatted_response += "*No specific key takeaways were identified.*"
                        
                    return formatted_response
                
                return str(actual_data)

            # Celery crashed or threw an exception
            elif current_status == "FAILURE":
                error_msg = status_data.get("error", "Unknown error")
                return f"❌ **Agent Execution Failed:**\n\n`{error_msg}`"

            # Task is still PENDING or PROCESSING
            else:
                # Update the UI dynamically if it's taking a long time
                if attempt > 5:
                    st.toast("Deep research taking longer than expected...", icon="⏳")
                
                # Wait 2 seconds before pinging the server again
                time.sleep(2)