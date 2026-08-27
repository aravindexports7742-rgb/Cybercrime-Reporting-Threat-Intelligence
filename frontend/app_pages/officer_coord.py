import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/handshake: Agency coordination")
st.caption("Log inter-agency coordination requests for active cases.")
st.space("small")

with st.container(border=True):
    cases_res = requests.get(f"{API_URL}/cases/", headers=get_headers())
    if cases_res.status_code == 200 and cases_res.json():
        cases_list    = cases_res.json()
        case_options  = {f"{c['case_reference']} (ID:{c['case_id']})": c["case_id"] for c in cases_list}
        selected_case = st.selectbox("Select case", list(case_options.keys()))
        case_id_coord = case_options[selected_case]
    else:
        case_id_coord = st.number_input("Case ID", min_value=1, value=1)

    org      = st.text_input("Organisation name", placeholder="Bank XYZ, Interpol, CERT-In…")
    req_type = st.text_input("Request type", placeholder="Freeze account, IP lookup, DNS block…")

    if st.button("Log request", icon=":material/send:", type="primary"):
        if org and req_type:
            res = requests.post(
                f"{API_URL}/cases/{case_id_coord}/coordination",
                headers=get_headers(),
                json={"organization_name": org, "request_type": req_type},
            )
            if res.status_code == 200:
                st.toast("Coordination request logged.", icon=":material/check_circle:")
            else:
                st.error(f"Failed: {res.text}", icon=":material/error:")
        else:
            st.warning("Please fill in both fields.", icon=":material/warning:")
