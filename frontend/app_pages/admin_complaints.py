import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

STATUS_BADGE = {
    "Submitted":    ("blue",   ":material/pending:"),
    "Under Review": ("blue",   ":material/manage_search:"),
    "Assigned":     ("violet", ":material/assignment_ind:"),
    "Investigation":("orange", ":material/search:"),
    "Action Taken": ("orange", ":material/gavel:"),
    "Resolved":     ("green",  ":material/check_circle:"),
    "Closed":       ("gray",   ":material/do_not_disturb:"),
}

st.subheader(":material/list_alt: All complaints — system-wide")
st.caption("Every complaint filed by all victims across the platform.")
st.space("small")

with st.skeleton(height=400):
    res = requests.get(f"{API_URL}/complaints/all", headers=get_headers())

if res.status_code == 200:
    complaints = res.json()
    if complaints:
        statuses = [c["status"] for c in complaints]
        with st.container(horizontal=True):
            st.metric("Total",             len(complaints), border=True)
            st.metric("Open",              sum(1 for s in statuses if s not in ["Resolved","Closed"]), border=True)
            st.metric("Resolved / Closed", sum(1 for s in statuses if s in ["Resolved","Closed"]), border=True)

        st.space("small")
        unique_statuses   = sorted(set(statuses))
        selected_statuses = st.pills("Filter by status", unique_statuses,
                                     selection_mode="multi", key="admin_status_pills")
        filtered = complaints if not selected_statuses else [c for c in complaints if c["status"] in selected_statuses]
        st.caption(f"Showing {len(filtered)} complaint(s)")
        st.space("small")

        for c in filtered:
            s_color, s_icon = STATUS_BADGE.get(c["status"], ("gray",":material/circle:"))
            with st.expander(f"[{c['tracking_id']}] {c['title']}", icon=s_icon):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Tracking ID:** `{c['tracking_id']}`")
                    st.markdown(f"**Complaint ID:** {c['complaint_id']}")
                    st.markdown(f"**Victim profile ID:** {c['victim_id']}")
                with col2:
                    st.markdown("**Status:**"); st.badge(c["status"], icon=s_icon, color=s_color)
                    st.markdown(f"**Financial loss:** ₹{c['financial_loss']:,.2f}")
                    st.markdown(f"**Filed on:** {str(c['created_at'])[:10]}")
                st.markdown(f"**Description:** {c['description']}")
                for label, key in [("Suspected URL","suspected_url"),("Suspected phone","suspected_phone"),("Suspected email","suspected_email")]:
                    if c.get(key): st.markdown(f"**{label}:** {c[key]}")
    else:
        st.info("No complaints filed yet.", icon=":material/info:")
else:
    st.error(f"Failed to load. (HTTP {res.status_code})", icon=":material/error:")
