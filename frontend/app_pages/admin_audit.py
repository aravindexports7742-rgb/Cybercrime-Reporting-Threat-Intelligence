import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/history: Audit logs")
st.caption("Complete audit trail of all platform actions.")
st.space("small")

with st.skeleton(height=300):
    res = requests.get(f"{API_URL}/admin/audit-logs", headers=get_headers())

if res.status_code == 200:
    logs = res.json()
    if logs:
        st.dataframe(pd.DataFrame(logs), hide_index=True)
    else:
        st.info("No audit logs available.", icon=":material/info:")
else:
    st.error("Failed to load audit logs.", icon=":material/error:")
