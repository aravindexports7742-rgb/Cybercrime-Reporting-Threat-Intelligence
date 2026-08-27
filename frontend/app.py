import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Cyber Platform", layout="wide", initial_sidebar_state="expanded")

# Injecting Custom CSS for a better design
st.markdown("""
<style>
    /* Global Font and styling */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1e3a8a !important; /* Dark Blue */
    }
    /* Buttons */
    .stButton>button {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background-color: #1d4ed8 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Form input styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>textarea, .stNumberInput>div>div>input {
        border-radius: 6px !important;
        border: 1px solid #d1d5db !important;
        padding: 8px 12px !important;
    }
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f3f4f6 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 6px 6px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e0f2fe !important;
        border-bottom: 3px solid #0284c7 !important;
        color: #0284c7 !important;
    }
    /* Success/Error banners */
    .stAlert {
        border-radius: 8px !important;
    }
    /* Background for main container */
    .main {
        background-color: #fafafa;
    }
    /* Footer or extra */
    .css-1v3fvcr {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)
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
    st.markdown("<h1 style='text-align: center;'>Cyber Crime & Threat Intelligence Platform</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b7280; margin-bottom: 2rem;'>Securely report and analyze cyber incidents.</p>", unsafe_allow_html=True)
    
    col_spacer1, col_main, col_spacer2 = st.columns([1, 2, 1])
    with col_main:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            st.markdown("### Welcome Back")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                login(email, password)
                
        with tab2:
            st.markdown("### Create an Account")
            with st.form("register_form"):
                reg_name = st.text_input("Full Name")
                reg_email = st.text_input("Email")
                reg_phone = st.text_input("Phone Number")
                reg_password = st.text_input("Password", type="password")
                reg_role = st.selectbox("Role", ["Victim", "Officer", "Threat Analyst", "Incident Responder", "Administrator"])
                
                if st.form_submit_button("Register", use_container_width=True):
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
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.markdown(f"<h2>Welcome to the Platform <span style='color: #6b7280; font-size: 1rem;'>(Role: {st.session_state['role']})</span></h2>", unsafe_allow_html=True)
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state["token"] = None
            st.session_state["role"] = None
            st.rerun()
            
    st.markdown("---")
    
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
