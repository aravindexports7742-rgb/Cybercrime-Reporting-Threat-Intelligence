import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/group: User management")
st.caption("View all users. Use the table to review details, or create a new user below.")
st.space("small")

with st.skeleton(height=300):
    res = requests.get(f"{API_URL}/admin/users", headers=get_headers())

if res.status_code == 200:
    users = res.json()
    if users:
        df = pd.DataFrame(users)
        # Use data_editor for inline viewing (read-only since we don't have a bulk update endpoint)
        st.data_editor(
            df,
            hide_index=True,
            use_container_width=False,
            disabled=True,
            key="users_table",
        )
    else:
        st.info("No users found.", icon=":material/info:")
else:
    st.error("Failed to load users.", icon=":material/error:")

st.space("small")
if st.session_state.get("role") != "Administrator":
    st.info("Incident Responders have view-only access to user records.", icon=":material/visibility:")
    st.stop()

with st.container(border=True):
    st.markdown("**:material/person_add: Create new user**")
    with st.form("create_user_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            u_name  = st.text_input("Full name",  placeholder="Jane Smith")
            u_email = st.text_input("Email",      placeholder="jane@org.com")
        with c2:
            u_phone = st.text_input("Phone",      placeholder="+91…")
            u_pass  = st.text_input("Password",   type="password", placeholder="••••••••")
        u_role = st.selectbox("Role", ["Victim","Officer","Threat Analyst","Incident Responder","Administrator"])
        if st.form_submit_button("Create user", icon=":material/person_add:", type="primary"):
            payload = {"full_name":u_name,"email":u_email,"phone_number":u_phone,"password":u_pass,"role_name":u_role}
            res2 = requests.post(f"{API_URL}/admin/users", headers=get_headers(), json=payload)
            if res2.status_code == 200:
                st.toast("User created.", icon=":material/check_circle:")
                st.rerun()
            else:
                st.error(f"Failed: {res2.text}", icon=":material/error:")
