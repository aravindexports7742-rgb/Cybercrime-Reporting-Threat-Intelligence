import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

PRIORITY_BADGE = {
    "Low":      ("green",  ":material/arrow_downward:"),
    "Medium":   ("yellow", ":material/remove:"),
    "High":     ("orange", ":material/arrow_upward:"),
    "Critical": ("red",    ":material/priority_high:"),
}

STATUS_BADGE = {
    "Submitted":               ("blue",   ":material/pending:"),
    "Under Review":            ("blue",   ":material/manage_search:"),
    "Assigned":                ("violet", ":material/assignment_ind:"),
    "Investigation":           ("orange", ":material/search:"),
    "Pending External Response":("yellow",":material/hourglass_empty:"),
    "Action Taken":            ("orange", ":material/gavel:"),
    "Resolved":                ("green",  ":material/check_circle:"),
    "Closed":                  ("gray",   ":material/do_not_disturb:"),
    "New":                     ("blue",   ":material/fiber_new:"),
}

def render():
    st.subheader(":material/local_police: Officer dashboard")
    st.caption("Manage active cases, investigate suspects, and coordinate with agencies.")
    st.space("small")

    tab_cases, tab_all, tab_suspects, tab_coord = st.tabs([
        ":material/folder_open: Active cases",
        ":material/list_alt: All complaints",
        ":material/person_search: Suspects",
        ":material/handshake: Agency coordination",
    ])

    # ── Tab 1: Active Cases ───────────────────────────────────────────────────
    with tab_cases:
        response = requests.get(f"{API_URL}/cases/", headers=get_headers())
        if response.status_code == 200:
            cases = response.json()
            if not cases:
                st.info(
                    "No cases found. Cases are auto-created when victims submit complaints.",
                    icon=":material/info:",
                )
            for c in cases:
                pri   = c["priority"]
                p_color, p_icon = PRIORITY_BADGE.get(pri, ("gray", ":material/circle:"))
                s_color, s_icon = STATUS_BADGE.get(c["status"], ("gray", ":material/circle:"))

                with st.expander(f"{c['case_reference']} — {c['status']}", icon=p_icon):
                    # Metric strip
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        with st.container(border=True):
                            st.caption("Case ID")
                            st.markdown(f"`{c['case_id']}`")
                    with m2:
                        with st.container(border=True):
                            st.caption("Priority")
                            st.badge(pri, icon=p_icon, color=p_color)
                    with m3:
                        with st.container(border=True):
                            st.caption("Opened")
                            st.markdown(str(c["opened_at"])[:10])

                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.markdown(f"**Status:**")
                        st.badge(c["status"], icon=s_icon, color=s_color)
                    with col_info2:
                        st.markdown(f"**Linked complaint ID:** {c.get('complaint_id', 'N/A')}")
                        if c.get("lead_officer_id"):
                            st.markdown(f"**Lead officer ID:** {c['lead_officer_id']}")

                    st.space("small")
                    with st.container(border=True):
                        st.markdown("**:material/edit: Update case**")
                        col_s, col_p = st.columns(2)
                        with col_s:
                            statuses = ["New","Under Review","Assigned","Investigation",
                                        "Pending External Response","Action Taken","Resolved","Closed"]
                            new_status = st.selectbox(
                                "Status",
                                statuses,
                                index=statuses.index(c["status"]),
                                key=f"status_{c['case_id']}",
                            )
                        with col_p:
                            priorities = ["Low","Medium","High","Critical"]
                            new_priority = st.selectbox(
                                "Priority",
                                priorities,
                                index=priorities.index(c["priority"]),
                                key=f"priority_{c['case_id']}",
                            )
                        if st.button("Save changes", icon=":material/save:", key=f"save_status_{c['case_id']}", type="primary"):
                            res = requests.put(
                                f"{API_URL}/cases/{c['case_id']}",
                                headers=get_headers(),
                                json={"status": new_status, "priority": new_priority},
                            )
                            if res.status_code == 200:
                                st.success("Case updated. Victim will be notified.", icon=":material/check_circle:")
                                st.rerun()
                            else:
                                st.error(f"Update failed: {res.text}", icon=":material/error:")

                    with st.container(border=True):
                        st.markdown("**:material/edit_note: Investigation notes**")
                        note_text = st.text_area(
                            "Add a note",
                            label_visibility="collapsed",
                            placeholder="Enter investigation notes here…",
                            key=f"note_{c['case_id']}",
                        )
                        if st.button("Add note", icon=":material/add:", key=f"add_note_{c['case_id']}"):
                            if note_text:
                                res = requests.post(
                                    f"{API_URL}/cases/{c['case_id']}/investigations",
                                    headers=get_headers(),
                                    json={"note_text": note_text},
                                )
                                if res.status_code == 200:
                                    st.success("Note added.", icon=":material/check_circle:")
                                    st.rerun()
                                else:
                                    st.error(f"Failed: {res.text}", icon=":material/error:")
                            else:
                                st.warning("Note cannot be empty.", icon=":material/warning:")
        else:
            st.error(f"Failed to load cases. (HTTP {response.status_code})", icon=":material/error:")

    # ── Tab 2: All Complaints ─────────────────────────────────────────────────
    with tab_all:
        st.subheader("All incoming complaints")
        st.caption("All complaints submitted by victims. A case is auto-created for each.")

        response = requests.get(f"{API_URL}/complaints/all", headers=get_headers())
        if response.status_code == 200:
            complaints = response.json()
            if not complaints:
                st.info("No complaints filed yet.", icon=":material/info:")
            else:
                col_a, col_b, col_c = st.columns(3)
                statuses = [c["status"] for c in complaints]
                col_a.metric("Total complaints", len(complaints))
                col_b.metric("Open", sum(1 for s in statuses if s not in ["Resolved","Closed"]))
                col_c.metric("Resolved / Closed", sum(1 for s in statuses if s in ["Resolved","Closed"]))

                st.space("small")
                all_statuses   = ["All"] + sorted(set(statuses))
                filter_status  = st.selectbox("Filter by status", all_statuses, key="officer_complaint_filter")
                filtered       = complaints if filter_status == "All" else [c for c in complaints if c["status"] == filter_status]
                st.caption(f"Showing {len(filtered)} complaint(s)")

                for c in filtered:
                    s_color, s_icon = STATUS_BADGE.get(c["status"], ("gray",":material/circle:"))
                    with st.expander(f"[{c['tracking_id']}] {c['title']}", icon=s_icon):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Tracking ID:** `{c['tracking_id']}`")
                            st.markdown(f"**Complaint ID:** {c['complaint_id']}")
                            st.markdown(f"**Victim profile ID:** {c['victim_id']}")
                        with col2:
                            st.markdown("**Status:**")
                            st.badge(c["status"], icon=s_icon, color=s_color)
                            st.markdown(f"**Financial loss:** ₹{c['financial_loss']:,.2f}")
                            st.markdown(f"**Filed on:** {str(c['created_at'])[:10]}")
                        st.markdown(f"**Description:** {c['description']}")
                        for label, key in [("Suspected URL","suspected_url"),("Suspected phone","suspected_phone"),("Suspected email","suspected_email")]:
                            if c.get(key):
                                st.markdown(f"**{label}:** {c[key]}")
        else:
            st.error(f"Failed to load complaints. (HTTP {response.status_code})", icon=":material/error:")

    # ── Tab 3: Suspects ───────────────────────────────────────────────────────
    with tab_suspects:
        st.subheader(":material/person_search: Add suspect")
        with st.container(border=True):
            with st.form("suspect_form", clear_on_submit=True):
                name       = st.text_input("Name / alias", placeholder="John Doe or @handle")
                contact    = st.text_input("Contact info", placeholder="phone, email, IP…")
                status_sus = st.selectbox("Status", ["Person of Interest","Confirmed","Cleared"])
                notes      = st.text_area("Notes", placeholder="Any relevant information…")
                if st.form_submit_button("Add suspect", icon=":material/add:", type="primary"):
                    payload = {
                        "name_alias":   name,
                        "contact_info": contact,
                        "status":       status_sus,
                        "notes":        notes,
                    }
                    res = requests.post(f"{API_URL}/cases/suspects", headers=get_headers(), json=payload)
                    if res.status_code == 200:
                        st.success("Suspect added.", icon=":material/check_circle:")
                    else:
                        st.error(f"Failed: {res.text}", icon=":material/error:")

    # ── Tab 4: Agency Coordination ────────────────────────────────────────────
    with tab_coord:
        st.subheader(":material/handshake: Log coordination request")
        with st.container(border=True):
            cases_res = requests.get(f"{API_URL}/cases/", headers=get_headers())
            if cases_res.status_code == 200 and cases_res.json():
                cases_list    = cases_res.json()
                case_options  = {f"{c['case_reference']} (ID:{c['case_id']})": c["case_id"] for c in cases_list}
                selected_case = st.selectbox("Select case", list(case_options.keys()))
                case_id_coord = case_options[selected_case]
            else:
                case_id_coord = st.number_input("Case ID for coordination", min_value=1, value=1)

            org      = st.text_input("Organisation name", placeholder="Bank XYZ, Interpol, CERT-In…")
            req_type = st.text_input("Request type", placeholder="Freeze account, IP lookup, DNS block…")

            if st.button("Log request", icon=":material/send:", type="primary"):
                if org and req_type:
                    payload = {"organization_name": org, "request_type": req_type}
                    res = requests.post(
                        f"{API_URL}/cases/{case_id_coord}/coordination",
                        headers=get_headers(), json=payload,
                    )
                    if res.status_code == 200:
                        st.success("Coordination request logged.", icon=":material/check_circle:")
                    else:
                        st.error(f"Failed: {res.text}", icon=":material/error:")
                else:
                    st.warning("Please fill in organisation name and request type.", icon=":material/warning:")
