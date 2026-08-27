import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

RISK_COLOR = {"Low":"green","Medium":"yellow","High":"orange","Critical":"red"}

st.subheader(":material/hub: Campaigns")
st.caption("Organised threat campaigns detected across multiple indicators.")
st.space("small")

with st.skeleton(height=300):
    res = requests.get(f"{API_URL}/campaigns", headers=get_headers())

if res.status_code == 200:
    campaigns = res.json()
    if campaigns:
        for c in campaigns:
            risk = c["risk_level"]
            with st.expander(c["campaign_name"], icon=":material/hub:"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Risk level:**")
                    st.badge(risk, color=RISK_COLOR.get(risk,"gray"))
                with col2:
                    st.markdown(f"**Detected:** {c['detected_at']}")
                st.markdown(f"**Description:** {c.get('description','N/A')}")
    else:
        with st.container(border=True):
            with st.container(horizontal_alignment="center"):
                st.markdown(":material/hub:")
                st.markdown("**No campaigns detected yet**")
else:
    st.error("Failed to load campaigns.", icon=":material/error:")
