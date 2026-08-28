import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/emergency: Active incidents")
st.caption("Manage and create security incidents.")
st.space("small")

with st.skeleton(height=300):
    res = requests.get(f"{API_URL}/admin/incidents", headers=get_headers())

if res.status_code == 200:
    incidents = res.json()
    if incidents:
        for incident in incidents:
            with st.expander(f"{incident['incident_reference']} — {incident['status']}", icon=":material/emergency:"):
                st.caption(f"Detected: {str(incident['detected_at'])[:16]} · Severity: {incident['severity']}")
                st.markdown(f"**Type:** {incident['incident_type']}")
                if incident.get("case_id"):
                    st.markdown(f"**Linked case:** {incident['case_id']}")
                st.markdown(f"**Current details:** {incident.get('description') or 'No details recorded.'}")
                with st.form(f"incident_update_{incident['incident_id']}"):
                    c1, c2 = st.columns(2)
                    statuses = ["Detected", "Triage", "Investigating", "Containing", "Remediating", "Recovering", "Resolved", "Closed"]
                    severities = ["Low", "Medium", "High", "Critical"]
                    with c1:
                        status = st.selectbox("Response stage", statuses, index=statuses.index(incident['status']))
                    with c2:
                        severity = st.selectbox("Severity", severities, index=severities.index(incident['severity']))
                    details = st.text_area("Progress update / response details", value=incident.get('description') or "", placeholder="Containment completed; affected access disabled. Next: validate recovery.")
                    if st.form_submit_button("Save incident progress", icon=":material/save:", type="primary"):
                        update = requests.put(
                            f"{API_URL}/admin/incidents/{incident['incident_id']}", headers=get_headers(),
                            json={"status": status, "severity": severity, "description": details},
                        )
                        if update.status_code == 200:
                            st.toast("Incident progress saved.", icon=":material/check_circle:")
                            st.rerun()
                        else:
                            st.error(f"Could not update incident: {update.text}", icon=":material/error:")
    else:
        st.info("No incidents found.", icon=":material/info:")
else:
    st.error("Failed to load incidents.", icon=":material/error:")

st.space("small")
with st.container(border=True):
    st.markdown("**:material/add_circle: Create incident manually**")
    with st.form("incident_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            ref      = st.text_input("Incident reference", placeholder="INC-2026-001")
            inc_type = st.text_input("Incident type",      placeholder="Ransomware, Phishing…")
        with c2:
            severity = st.selectbox("Severity", ["Low","Medium","High","Critical"])
        desc = st.text_area("Description", placeholder="What happened?")
        if st.form_submit_button("Create incident", icon=":material/emergency:", type="primary"):
            if ref and inc_type:
                payload = {"incident_reference":ref,"incident_type":inc_type,"description":desc,"severity":severity,"status":"Detected"}
                res2 = requests.post(f"{API_URL}/admin/incidents", headers=get_headers(), json=payload)
                if res2.status_code == 200:
                    st.toast("Incident created.", icon=":material/check_circle:")
                    st.rerun()
                else:
                    st.error(f"Failed: {res2.text}", icon=":material/error:")
            else:
                st.warning("Reference and type are required.", icon=":material/warning:")
