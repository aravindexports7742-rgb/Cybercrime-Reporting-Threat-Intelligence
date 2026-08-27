import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/person_search: Suspects")
st.caption("Register persons of interest linked to cases.")
st.space("small")

with st.container(border=True):
    st.markdown("**:material/person_add: Add new suspect**")
    with st.form("suspect_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name    = st.text_input("Name / alias", placeholder="John Doe or @handle")
            contact = st.text_input("Contact info", placeholder="phone, email, IP…")
        with c2:
            status_sus = st.selectbox("Status", ["Person of Interest","Confirmed","Cleared"])
        notes = st.text_area("Notes", placeholder="Any relevant information…")
        if st.form_submit_button("Add suspect", icon=":material/add:", type="primary"):
            payload = {"name_alias": name, "contact_info": contact, "status": status_sus, "notes": notes}
            res = requests.post(f"{API_URL}/cases/suspects", headers=get_headers(), json=payload)
            if res.status_code == 200:
                st.success("Suspect added.", icon=":material/check_circle:")
            else:
                st.error(f"Failed: {res.text}", icon=":material/error:")
