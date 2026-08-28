import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/rss_feed: Threat feeds")
st.caption("External and internal threat intelligence feeds ingested into the platform.")
st.space("small")

with st.skeleton(height=300):
    res = requests.get(f"{API_URL}/threat-feeds", headers=get_headers())

if res.status_code == 200:
    feeds = res.json()
    if feeds:
        st.dataframe(pd.DataFrame(feeds), hide_index=True)
    else:
        with st.container(border=True):
            with st.container(horizontal_alignment="center"):
                st.markdown(":material/rss_feed:")
                st.markdown("**No threat feeds ingested yet**")
                st.caption("Configure feed sources in your backend to start seeing data here.")
else:
    st.error("Failed to load feeds.", icon=":material/error:")
