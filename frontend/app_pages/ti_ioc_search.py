import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/search: IOC search")
st.caption("Search the database for known indicators of compromise or register new ones.")
st.space("small")

with st.container(border=True):
    st.markdown("**:material/search: Search**")
    with st.container(horizontal=True, vertical_alignment="bottom"):
        search_val = st.text_input("Indicator value", label_visibility="collapsed",
                                   placeholder="IP, domain, URL, hash, or email…")
        search_btn = st.button("Search", icon=":material/search:", type="primary")
    if search_btn and search_val:
        with st.skeleton(height=200):
            res = requests.get(f"{API_URL}/iocs/search", headers=get_headers(), params={"value": search_val})
        if res.status_code == 200:
            results = res.json()
            if results:
                st.dataframe(pd.DataFrame(results), hide_index=True)
            else:
                st.info("No matching IOCs found.", icon=":material/info:")
        else:
            st.error("Search failed.", icon=":material/error:")

st.space("small")
with st.container(border=True):
    st.markdown("**:material/add_circle: Register new IOC**")
    with st.form("ioc_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1: ioc_type  = st.selectbox("IOC type",   ["IP","Domain","URL","Hash","Email"])
        with c2: ioc_value = st.text_input("IOC value",  placeholder="e.g. 192.168.1.1")
        with c3: risk_level = st.selectbox("Risk level", ["Low","Medium","High","Critical"])
        if st.form_submit_button("Register IOC", icon=":material/add:", type="primary") and ioc_value:
            payload = {"ioc_type": ioc_type, "ioc_value": ioc_value, "risk_level": risk_level}
            res = requests.post(f"{API_URL}/iocs", headers=get_headers(), json=payload)
            if res.status_code == 200:
                st.toast(f"IOC registered: {ioc_value}", icon=":material/check_circle:")
            else:
                st.error(f"Failed: {res.text}", icon=":material/error:")
