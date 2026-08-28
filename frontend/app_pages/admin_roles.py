import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/badge: Roles & permissions")
st.caption("Overview of all roles in the platform.")
st.space("small")

with st.skeleton(height=200):
    res = requests.get(f"{API_URL}/admin/roles", headers=get_headers())

if res.status_code == 200:
    roles = res.json()
    if roles:
        st.dataframe(pd.DataFrame(roles), hide_index=True)
    else:
        st.info("No roles found.", icon=":material/info:")
else:
    st.error("Failed to load roles.", icon=":material/error:")
