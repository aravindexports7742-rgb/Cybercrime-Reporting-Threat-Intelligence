import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

HEALTH_BADGE = {
    "Healthy": ("green",  ":material/check_circle:"),
    "Warning": ("orange", ":material/warning:"),
    "Critical":("red",    ":material/error:"),
}

st.subheader(":material/monitor_heart: System health")
st.caption("Real-time health status of all platform components.")
st.space("small")

with st.skeleton(height=300):
    res = requests.get(f"{API_URL}/admin/system-health", headers=get_headers())

if res.status_code == 200:
    health = res.json()
    if health:
        # Badge grid
        cols_h = st.columns(min(len(health), 3))
        for i, h in enumerate(health):
            color, icon = HEALTH_BADGE.get(h["status"],("gray",":material/circle:"))
            with cols_h[i % 3]:
                with st.container(border=True):
                    st.markdown(f"**{h['component_name']}**")
                    st.badge(h["status"], icon=icon, color=color)
                    if h.get("details"):
                        st.caption(h["details"])
        st.space("small")
        st.markdown("**Raw health data**")
        st.dataframe(pd.DataFrame(health), hide_index=True)
    else:
        st.info("No health records found.", icon=":material/info:")
else:
    st.error("Failed to load system health.", icon=":material/error:")
