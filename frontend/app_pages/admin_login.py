import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/login: Login activity")
st.caption("Authentication history across all users.")
st.space("small")

with st.skeleton(height=300):
    res = requests.get(f"{API_URL}/admin/login-history", headers=get_headers())

if res.status_code == 200:
    history = res.json()
    if history:
        st.dataframe(pd.DataFrame(history), hide_index=True)
    else:
        st.info("No login history available.", icon=":material/info:")
else:
    st.error("Failed to load login history.", icon=":material/error:")
