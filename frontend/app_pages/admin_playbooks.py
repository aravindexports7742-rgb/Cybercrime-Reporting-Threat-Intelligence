import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/menu_book: Response playbooks")
st.caption("Standard operating procedures for cybercrime incident response.")
st.space("small")

with st.skeleton(height=300):
    res = requests.get(f"{API_URL}/admin/playbooks", headers=get_headers())

if res.status_code == 200:
    playbooks = res.json()
    if playbooks:
        for p in playbooks:
            with st.expander(p["playbook_name"], icon=":material/menu_book:"):
                st.caption(f"Incident type: {p.get('incident_type','Any')}")
                st.markdown(p.get("description","No description."))
                st.markdown("**Steps:**")
                for step in p.get("steps",[]):
                    st.markdown(f"{step['step_order']}. {step['step_description']}")
    else:
        with st.container(border=True):
            with st.container(horizontal_alignment="center"):
                st.markdown(":material/menu_book:")
                st.markdown("**No playbooks defined yet**")
                st.caption("Contact your administrator to add response playbooks.")
else:
    st.error("Failed to load playbooks.", icon=":material/error:")
