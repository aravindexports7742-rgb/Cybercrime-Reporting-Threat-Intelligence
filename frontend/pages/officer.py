import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

def render():
    st.markdown("<h2>🚔 Officer Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; font-size: 1.1rem; margin-bottom: 1.5rem;'>Manage active cases, investigate suspects, and coordinate with agencies.</p>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Active Cases", "📋 All Complaints", "🕵️ Suspects", "🤝 Agency Coordination"
    ])

    # ── Tab 1: Active Cases ───────────────────────────────────────────────────
    with tab1:
        st.subheader("Active Cases")
        response = requests.get(f"{API_URL}/cases/", headers=get_headers())
        if response.status_code == 200:
            cases = response.json()
            if not cases:
                st.info("No cases found. Cases are automatically created when victims submit complaints.")
            for c in cases:
                priority_emoji = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}.get(c["priority"], "⚪")
                with st.expander(
                    f"{priority_emoji} {c['case_reference']} — Priority: {c['priority']} | Status: {c['status']}"
                ):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Case ID:** `{c['case_id']}`")
                        st.write(f"**Opened:** {str(c['opened_at'])[:10]}")
                    with col2:
                        st.write(f"**Status:** {c['status']}")
                        st.write(f"**Priority:** {c['priority']}")
                    with col3:
                        st.write(f"**Linked Complaint ID:** {c.get('complaint_id', 'N/A')}")
                        if c.get("lead_officer_id"):
                            st.write(f"**Lead Officer ID:** {c['lead_officer_id']}")

                    st.markdown("---")
                    col_s, col_p = st.columns(2)
                    with col_s:
                        new_status = st.selectbox(
                            "Update Status",
                            ["New", "Under Review", "Assigned", "Investigation",
                             "Pending External Response", "Action Taken", "Resolved", "Closed"],
                            index=["New", "Under Review", "Assigned", "Investigation",
                                   "Pending External Response", "Action Taken", "Resolved", "Closed"].index(c["status"]),
                            key=f"status_{c['case_id']}"
                        )
                    with col_p:
                        new_priority = st.selectbox(
                            "Update Priority",
                            ["Low", "Medium", "High", "Critical"],
                            index=["Low", "Medium", "High", "Critical"].index(c["priority"]),
                            key=f"priority_{c['case_id']}"
                        )
                    if st.button("💾 Save Changes", key=f"save_status_{c['case_id']}"):
                        res = requests.put(
                            f"{API_URL}/cases/{c['case_id']}",
                            headers=get_headers(),
                            json={"status": new_status, "priority": new_priority}
                        )
                        if res.status_code == 200:
                            st.success("✅ Case updated! Victim will be notified automatically.")
                            st.rerun()
                        else:
                            st.error(f"Update failed: {res.text}")

                    st.markdown("---")
                    st.subheader("📝 Investigation Notes")
                    note_text = st.text_area("Add a note", key=f"note_{c['case_id']}")
                    if st.button("➕ Add Note", key=f"add_note_{c['case_id']}"):
                        if note_text:
                            res = requests.post(
                                f"{API_URL}/cases/{c['case_id']}/investigations",
                                headers=get_headers(),
                                json={"note_text": note_text}
                            )
                            if res.status_code == 200:
                                st.success("Note added successfully.")
                                st.rerun()
                            else:
                                st.error(f"Failed: {res.text}")
                        else:
                            st.warning("Note cannot be empty.")
        else:
            st.error(f"Failed to load cases. (HTTP {response.status_code})")

    # ── Tab 2: All Complaints (full details) ──────────────────────────────────
    with tab2:
        st.subheader("All Incoming Complaints")
        st.info("All complaints submitted by victims — full details. A case is auto-created for each complaint.")

        response = requests.get(f"{API_URL}/complaints/all", headers=get_headers())
        if response.status_code == 200:
            complaints = response.json()
            if not complaints:
                st.info("No complaints filed yet.")
            else:
                st.write(f"**Total Complaints:** {len(complaints)}")
                st.divider()
                for c in complaints:
                    status_emoji = {
                        "Submitted": "🟡", "Under Review": "🔵", "Assigned": "🟣",
                        "Investigation": "🔍", "Action Taken": "🟠", "Resolved": "✅", "Closed": "⚫"
                    }.get(c["status"], "⚪")
                    with st.expander(
                        f"{status_emoji} [{c['tracking_id']}] {c['title']} — Status: {c['status']}"
                    ):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Tracking ID:** `{c['tracking_id']}`")
                            st.write(f"**Complaint ID:** {c['complaint_id']}")
                            st.write(f"**Victim Profile ID:** {c['victim_id']}")
                            st.write(f"**Category ID:** {c['category_id']}")
                        with col2:
                            st.write(f"**Status:** {c['status']}")
                            st.write(f"**Financial Loss:** ₹{c['financial_loss']}")
                            st.write(f"**Incident Date:** {c['incident_date']}")
                            st.write(f"**Filed On:** {str(c['created_at'])[:10]}")
                        st.write(f"**Description:** {c['description']}")
                        if c.get("suspected_url"):
                            st.write(f"**Suspected URL:** {c['suspected_url']}")
                        if c.get("suspected_phone"):
                            st.write(f"**Suspected Phone:** {c['suspected_phone']}")
                        if c.get("suspected_email"):
                            st.write(f"**Suspected Email:** {c['suspected_email']}")
        else:
            st.error(f"Failed to load complaints. (HTTP {response.status_code})")

    # ── Tab 3: Suspects ───────────────────────────────────────────────────────
    with tab3:
        st.subheader("🕵️ Manage Suspects")
        with st.form("suspect_form", clear_on_submit=True):
            name = st.text_input("Name / Alias")
            contact = st.text_input("Contact Info")
            status_sus = st.selectbox("Status", ["Person of Interest", "Confirmed", "Cleared"])
            notes = st.text_area("Notes")

            submit = st.form_submit_button("➕ Add Suspect")
            if submit:
                payload = {
                    "name_alias": name,
                    "contact_info": contact,
                    "status": status_sus,
                    "notes": notes,
                }
                res = requests.post(f"{API_URL}/cases/suspects", headers=get_headers(), json=payload)
                if res.status_code == 200:
                    st.success("✅ Suspect added successfully.")
                else:
                    st.error(f"Failed to add suspect: {res.text}")

    # ── Tab 4: Agency Coordination ────────────────────────────────────────────
    with tab4:
        st.subheader("🤝 Agency Coordination")

        # Fetch cases to select from
        cases_res = requests.get(f"{API_URL}/cases/", headers=get_headers())
        if cases_res.status_code == 200 and cases_res.json():
            cases_list = cases_res.json()
            case_options = {f"{c['case_reference']} (ID:{c['case_id']})": c["case_id"] for c in cases_list}
            selected_case_label = st.selectbox("Select Case", list(case_options.keys()))
            case_id_coord = case_options[selected_case_label]
        else:
            case_id_coord = st.number_input("Case ID for Coordination", min_value=1, value=1)

        org = st.text_input("Organization Name (e.g. Bank XYZ, Interpol)")
        req_type = st.text_input("Request Type (e.g. Freeze Account, IP Lookup)")
        if st.button("📤 Log Coordination Request"):
            if org and req_type:
                payload = {"organization_name": org, "request_type": req_type}
                res = requests.post(
                    f"{API_URL}/cases/{case_id_coord}/coordination",
                    headers=get_headers(), json=payload
                )
                if res.status_code == 200:
                    st.success("✅ Coordination request logged successfully.")
                else:
                    st.error(f"Failed: {res.text}")
            else:
                st.warning("Please fill in Organization Name and Request Type.")
