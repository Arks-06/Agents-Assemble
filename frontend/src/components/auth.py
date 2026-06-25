import streamlit as st
from api_client import login_user, register_user

def render_auth_page():
    st.title("Welcome to Agents Assemble 🤖")
    st.markdown("Please log in or create an account to access the workspace.")
    
    # two clean tabs
    tab1, tab2 = st.tabs(["🔒 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Login")
        with st.form("login_form"):
            login_email = st.text_input("Email")
            login_password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Login")
            
            if submit_login:
                if not login_email or not login_password:
                    st.warning("Please fill in all fields.")
                else:
                    with st.spinner("Authenticating..."):
                        token = login_user(login_email, login_password)
                        if token:
                            # Saves the token and trigger a UI rerun
                            st.session_state["access_token"] = token
                            st.rerun()
                        else:
                            st.error("Invalid email or password.")
                            
    with tab2:
        st.subheader("Create an Account")
        with st.form("register_form"):
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Password", type="password")
            reg_confirm = st.text_input("Confirm Password", type="password")
            submit_register = st.form_submit_button("Register")
            
            if submit_register:
                if not reg_email or not reg_password:
                    st.warning("Please fill in all fields.")
                elif reg_password != reg_confirm:
                    st.error("Passwords do not match.")
                else:
                    with st.spinner("Creating account..."):
                        success = register_user(reg_email, reg_password)
                        if success:
                            st.success("Account created successfully! Please switch to the Login tab.")
                        else:
                            st.error("Registration failed. Email might already exist.")