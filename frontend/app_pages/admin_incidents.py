import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/emergency: Active incidents")
st.caption("Manage and create security incidents.")
st.space("small")

with st.skeleton(height=300):
    res = requests.get(f"{API_URL}/admin/incidents", headers=get_headers())

if res.status_code == 200:
    incidents = res.json()
    if incidents:
        st.dataframe(pd.DataFrame(incidents), hide_index=True)
    else:
        st.info("No incidents found.", icon=":material/info:")
else:
    st.error("Failed to load incidents.", icon=":material/error:")

st.space("small")
with st.container(border=True):
    st.markdown("**:material/add_circle: Create incident manually**")
    with st.form("incident_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            ref      = st.text_input("Incident reference", placeholder="INC-2026-001")
            inc_type = st.text_input("Incident type",      placeholder="Ransomware, Phishing…")
        with c2:
            severity = st.selectbox("Severity", ["Low","Medium","High","Critical"])
        desc = st.text_area("Description", placeholder="What happened?")
        if st.form_submit_button("Create incident", icon=":material/emergency:", type="primary"):
            if ref and inc_type:
                payload = {"incident_reference":ref,"incident_type":inc_type,"description":desc,"severity":severity,"status":"Detected"}
                res2 = requests.post(f"{API_URL}/admin/incidents", headers=get_headers(), json=payload)
                if res2.status_code == 200:
                    st.toast("Incident created.", icon=":material/check_circle:")
                    st.rerun()
                else:
                    st.error(f"Failed: {res2.text}", icon=":material/error:")
            else:
                st.warning("Reference and type are required.", icon=":material/warning:")
