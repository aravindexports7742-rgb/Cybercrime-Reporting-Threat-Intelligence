import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Cyber Platform", layout="wide")

if "token" not in st.session_state:
    st.session_state["token"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None

def login(email, password):
    response = requests.post(f"{API_URL}/auth/login", data={"username": email, "password": password})
    if response.status_code == 200:
        data = response.json()
        st.session_state["token"] = data["access_token"]
        st.session_state["role"] = data.get("role", "Victim")
        st.success("Logged in successfully!")
        st.rerun()
    else:
        st.error("Login failed. Check credentials.")

if st.session_state["token"] is None:
    st.title("Cyber Crime & Threat Intelligence Platform")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login(email, password)
            
    with tab2:
        st.subheader("Register")
        with st.form("register_form"):
            reg_name = st.text_input("Full Name")
            reg_email = st.text_input("Email")
            reg_phone = st.text_input("Phone Number")
            reg_password = st.text_input("Password", type="password")
            reg_role = st.selectbox("Role", ["Victim", "Officer", "Threat Analyst", "Incident Responder", "Administrator"])
            
            if st.form_submit_button("Register"):
                payload = {
                    "full_name": reg_name,
                    "email": reg_email,
                    "phone_number": reg_phone,
                    "password": reg_password,
                    "role_name": reg_role
                }
                res = requests.post(f"{API_URL}/auth/register", json=payload)
                if res.status_code == 200:
                    st.success("Registered successfully! You can now log in.")
                else:
                    st.error(f"Registration failed: {res.text}")
else:
    st.title(f"Welcome to the Platform (Role: {st.session_state['role']})")
    if st.button("Logout"):
        st.session_state["token"] = None
        st.session_state["role"] = None
        st.rerun()
    
    if st.session_state["role"] == "Victim":
        from pages import victim
        victim.render()
    elif st.session_state["role"] == "Officer":
        from pages import officer
        officer.render()
    elif st.session_state["role"] == "Threat Analyst":
        from pages import threat_intel
        threat_intel.render()
    elif st.session_state["role"] in ["Administrator", "Incident Responder"]:
        from pages import admin
        admin.render()
    else:
        st.write("Navigation to sectors based on role will go here.")
