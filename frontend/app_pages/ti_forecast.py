import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/auto_graph: Threat forecast")
st.caption("IOC volume statistics and daily average trends.")
st.space("small")

with st.skeleton(height=200):
    res = requests.get(f"{API_URL}/threat-forecast", headers=get_headers())

if res.status_code == 200:
    data = res.json()
    with st.container(border=True):
        st.markdown("**IOC volume summary**")
        with st.container(horizontal=True):
            st.metric("Total IOCs",   data["total_iocs"],   border=True)
            st.metric("Last 7 days",  data["last_7_days"],  border=True)
            st.metric("Last 30 days", data["last_30_days"], border=True)
    st.space("small")
    with st.container(border=True):
        st.markdown("**Daily averages**")
        with st.container(horizontal=True):
            st.metric("Avg daily (7d)",  data["avg_daily_7d"],  border=True)
            st.metric("Avg daily (30d)", data["avg_daily_30d"], border=True)
else:
    st.error("Failed to load forecast.", icon=":material/error:")
