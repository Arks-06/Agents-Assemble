import httpx
import streamlit as st
from config import settings

def get_headers():
    """Retrieves the token from session state and formats the header."""
    token = st.session_state.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def start_research_task(topic: str) -> str | None:
    try:
        response = httpx.post(
            f"{settings.BACKEND_URL}/api/agents/research", 
            json={"topic": topic}, 
            headers=get_headers(), 
            timeout=10.0
        )
        response.raise_for_status()
        return response.json().get("task_id")
    except Exception as e:
        print(f"API Error (Dispatch): {e}")
        return None

def fetch_task_status(task_id: str) -> dict | None:
    """Polls the backend for the current status of the Celery task."""
    try:
        response = httpx.get(
            
            f"{settings.BACKEND_URL}/api/agents/research/status/{task_id}", 
            headers=get_headers(), 
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API Error (Poll): {e}")
        return None
    

def login_user(email: str, password: str) -> str | None:
    """Authenticates the user and returns the JWT token."""
    try:
        # FastAPI OAuth2PasswordRequestForm STRICTLY expects form data, not json
        payload = {"username": email, "password": password}
        response = httpx.post(
            f"{settings.BACKEND_URL}/api/auth/login", 
            data=payload, 
            timeout=10.0
        )
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        print(f"Login Error: {e}")
        return None

def register_user(email: str, password: str) -> bool:
    """Registers a new user. Returns True if successful."""
    try:
        payload = {"email": email, "password": password}
        response = httpx.post(
            f"{settings.BACKEND_URL}/api/auth/register", 
            json=payload, 
            timeout=10.0
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Registration Error: {e}")
        return False