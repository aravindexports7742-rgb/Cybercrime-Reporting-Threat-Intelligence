import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

def render():
    st.header("🔐 Admin & SOC Dashboard")

    tabs = st.tabs([
        "📊 Overview", "📋 All Complaints", "🚨 Active Incidents",
        "📖 Response Playbooks", "👥 Users", "🎭 Roles & Permissions",
        "📜 Audit Logs", "🔑 Login Activity", "💻 System Health"
    ])

    # ── Tab 0: Overview ───────────────────────────────────────────────────────
    with tabs[0]:
        st.subheader("Platform Overview")
        col1, col2, col3 = st.columns(3)

        # Complaint metrics
        with col1:
            st.markdown("**📋 Complaint Summary**")
            res = requests.get(f"{API_URL}/complaints/all", headers=get_headers())
            if res.status_code == 200:
                complaints = res.json()
                open_c = [c for c in complaints if c["status"] not in ["Resolved", "Closed"]]
                st.metric("Total Complaints", len(complaints))
                st.metric("Open Complaints", len(open_c))
            else:
                st.error("Failed to load complaint metrics")

        # Incident metrics
        with col2:
            st.markdown("**🚨 Incident Summary**")
            res = requests.get(f"{API_URL}/admin/incidents", headers=get_headers())
            if res.status_code == 200:
                incidents = res.json()
                active = [i for i in incidents if i["status"] not in ["Resolved", "Closed"]]
                st.metric("Total Incidents", len(incidents))
                st.metric("Active Incidents", len(active))
            else:
                st.error("Failed to load incident metrics")

        # System health
        with col3:
            st.markdown("**💻 System Health**")
            res = requests.get(f"{API_URL}/admin/system-health", headers=get_headers())
            if res.status_code == 200:
                health = res.json()
                if health:
                    for h in health:
                        color = "green" if h["status"] == "Healthy" else "orange" if h["status"] == "Warning" else "red"
                        st.markdown(f"- **{h['component_name']}**: :{color}[{h['status']}]")
                else:
                    st.info("No recent health checks recorded.")
            else:
                st.error("Failed to load health metrics")

    # ── Tab 1: All Complaints ─────────────────────────────────────────────────
    with tabs[1]:
        st.subheader("All Complaints (System-wide)")
        st.info("Every complaint filed by all victims across the platform.")

        res = requests.get(f"{API_URL}/complaints/all", headers=get_headers())
        if res.status_code == 200:
            complaints = res.json()
            if complaints:
                # Summary metrics
                col_a, col_b, col_c = st.columns(3)
                statuses = [c["status"] for c in complaints]
                col_a.metric("Total", len(complaints))
                col_b.metric("Open", sum(1 for s in statuses if s not in ["Resolved", "Closed"]))
                col_c.metric("Resolved / Closed", sum(1 for s in statuses if s in ["Resolved", "Closed"]))

                st.divider()

                # Filter by status
                all_statuses = ["All"] + sorted(set(statuses))
                filter_status = st.selectbox("Filter by Status", all_statuses, key="admin_complaint_filter")
                filtered = complaints if filter_status == "All" else [c for c in complaints if c["status"] == filter_status]

                st.write(f"Showing **{len(filtered)}** complaint(s)")
                for c in filtered:
                    status_emoji = {
                        "Submitted": "🟡", "Under Review": "🔵", "Assigned": "🟣",
                        "Investigation": "🔍", "Action Taken": "🟠", "Resolved": "✅", "Closed": "⚫"
                    }.get(c["status"], "⚪")
                    with st.expander(
                        f"{status_emoji} [{c['tracking_id']}] {c['title']} — {c['status']}"
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
                st.info("No complaints filed yet.")
        else:
            st.error(f"Failed to load complaints. (HTTP {res.status_code})")

    # ── Tab 2: Active Incidents ───────────────────────────────────────────────
    with tabs[2]:
        st.subheader("Active Incidents")
        res = requests.get(f"{API_URL}/admin/incidents", headers=get_headers())
        if res.status_code == 200:
            incidents = res.json()
            if incidents:
                df = pd.DataFrame(incidents)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No incidents found.")
        else:
            st.error("Failed to load incidents")

        st.divider()
        st.subheader("Create Incident Manually")
        with st.form("incident_form", clear_on_submit=True):
            ref = st.text_input("Incident Reference (e.g. INC-2026-001)")
            inc_type = st.text_input("Incident Type (e.g. Ransomware, Phishing)")
            desc = st.text_area("Description")
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            submitted = st.form_submit_button("🚨 Create Incident")
            if submitted and ref and inc_type:
                payload = {
                    "incident_reference": ref,
                    "incident_type": inc_type,
                    "description": desc,
                    "severity": severity,
                    "status": "Detected"
                }
                res = requests.post(f"{API_URL}/admin/incidents", headers=get_headers(), json=payload)
                if res.status_code == 200:
                    st.success("✅ Incident created successfully.")
                    st.rerun()
                else:
                    st.error(f"Failed to create incident: {res.text}")

    # ── Tab 3: Response Playbooks ─────────────────────────────────────────────
    with tabs[3]:
        st.subheader("Response Playbooks")
        res = requests.get(f"{API_URL}/admin/playbooks", headers=get_headers())
        if res.status_code == 200:
            playbooks = res.json()
            if playbooks:
                for p in playbooks:
                    with st.expander(f"📖 {p['playbook_name']} (Type: {p.get('incident_type', 'Any')})"):
                        st.write(p.get("description", "No description."))
                        st.markdown("**Steps:**")
                        for step in p.get("steps", []):
                            st.write(f"{step['step_order']}. {step['step_description']}")
            else:
                st.info("No playbooks defined yet.")
        else:
            st.error("Failed to load playbooks.")

    # ── Tab 4: Users ──────────────────────────────────────────────────────────
    with tabs[4]:
        st.subheader("User Management")
        res = requests.get(f"{API_URL}/admin/users", headers=get_headers())
        if res.status_code == 200:
            users = res.json()
            if users:
                st.dataframe(pd.DataFrame(users), use_container_width=True)
            else:
                st.info("No users found.")
        else:
            st.error("Failed to load users.")

        st.divider()
        st.subheader("Create New User")
        with st.form("create_user_form", clear_on_submit=True):
            u_name = st.text_input("Full Name")
            u_email = st.text_input("Email")
            u_phone = st.text_input("Phone")
            u_pass = st.text_input("Password", type="password")
            u_role = st.selectbox("Role", ["Victim", "Officer", "Threat Analyst", "Incident Responder", "Administrator"])
            if st.form_submit_button("➕ Create User"):
                payload = {
                    "full_name": u_name, "email": u_email,
                    "phone_number": u_phone, "password": u_pass, "role_name": u_role
                }
                res = requests.post(f"{API_URL}/admin/users", headers=get_headers(), json=payload)
                if res.status_code == 200:
                    st.success("✅ User created.")
                    st.rerun()
                else:
                    st.error(f"Failed: {res.text}")

    # ── Tab 5: Roles & Permissions ────────────────────────────────────────────
    with tabs[5]:
        st.subheader("Roles Overview")
        res = requests.get(f"{API_URL}/admin/roles", headers=get_headers())
        if res.status_code == 200:
            roles = res.json()
            if roles:
                st.dataframe(pd.DataFrame(roles), use_container_width=True)
            else:
                st.info("No roles found.")
        else:
            st.error("Failed to load roles.")

    # ── Tab 6: Audit Logs ─────────────────────────────────────────────────────
    with tabs[6]:
        st.subheader("Platform Audit Logs")
        res = requests.get(f"{API_URL}/admin/audit-logs", headers=get_headers())
        if res.status_code == 200:
            logs = res.json()
            if logs:
                st.dataframe(pd.DataFrame(logs), use_container_width=True)
            else:
                st.info("No audit logs available.")
        else:
            st.error("Failed to load audit logs.")

    # ── Tab 7: Login Activity ─────────────────────────────────────────────────
    with tabs[7]:
        st.subheader("Login History")
        res = requests.get(f"{API_URL}/admin/login-history", headers=get_headers())
        if res.status_code == 200:
            history = res.json()
            if history:
                st.dataframe(pd.DataFrame(history), use_container_width=True)
            else:
                st.info("No login history available.")
        else:
            st.error("Failed to load login history.")

    # ── Tab 8: System Health ──────────────────────────────────────────────────
    with tabs[8]:
        st.subheader("Detailed System Health")
        res = requests.get(f"{API_URL}/admin/system-health", headers=get_headers())
        if res.status_code == 200:
            health = res.json()
            if health:
                st.dataframe(pd.DataFrame(health), use_container_width=True)
            else:
                st.info("No health records found.")
        else:
            st.error("Failed to load system health.")
