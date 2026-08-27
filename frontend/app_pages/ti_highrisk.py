import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/warning: High-risk indicators")
st.caption("Showing High and Critical severity IOCs only.")
st.space("small")

with st.skeleton(height=300):
    res = requests.get(f"{API_URL}/threats", headers=get_headers())

if res.status_code == 200:
    threats = res.json()
    if threats:
        st.badge(f"{len(threats)} high-risk IOCs", icon=":material/warning:", color="red")
        st.space("small")
        st.dataframe(pd.DataFrame(threats), hide_index=True)
    else:
        st.success("No high-risk indicators found.", icon=":material/check_circle:")
else:
    st.error("Failed to load threats.", icon=":material/error:")
