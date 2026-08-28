import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

STATUS_BADGE = {
    "Submitted":   ("blue",   ":material/pending:"),
    "Under Review":("blue",   ":material/manage_search:"),
    "Assigned":    ("violet", ":material/assignment_ind:"),
    "Investigation":("orange",":material/search:"),
    "Action Taken":("orange", ":material/gavel:"),
    "Resolved":    ("green",  ":material/check_circle:"),
    "Closed":      ("gray",   ":material/do_not_disturb:"),
}

HEALTH_BADGE = {
    "Healthy": ("green",  ":material/check_circle:"),
    "Warning": ("orange", ":material/warning:"),
    "Critical":("red",    ":material/error:"),
}

def render():
    st.subheader(":material/admin_panel_settings: Admin & SOC dashboard")
    st.caption("Platform overview, incident management, and system administration.")
    st.space("small")

    tabs = st.tabs([
        ":material/dashboard: Overview",
        ":material/list_alt: All complaints",
        ":material/emergency: Active incidents",
        ":material/menu_book: Playbooks",
        ":material/group: Users",
        ":material/badge: Roles",
        ":material/history: Audit logs",
        ":material/login: Login activity",
        ":material/monitor_heart: System health",
    ])

    # ── Tab 0: Overview ───────────────────────────────────────────────────────
    with tabs[0]:
        st.subheader("Platform overview")

        res_comp  = requests.get(f"{API_URL}/complaints/all",       headers=get_headers())
        res_inc   = requests.get(f"{API_URL}/admin/incidents",      headers=get_headers())
        res_hlth  = requests.get(f"{API_URL}/admin/system-health",  headers=get_headers())

        complaints = res_comp.json()  if res_comp.status_code == 200  else []
        incidents  = res_inc.json()   if res_inc.status_code  == 200  else []
        health_chk = res_hlth.json()  if res_hlth.status_code == 200  else []

        open_c  = [c for c in complaints if c["status"] not in ["Resolved","Closed"]]
        active_i = [i for i in incidents  if i["status"] not in ["Resolved","Closed"]]
        healthy  = sum(1 for h in health_chk if h["status"] == "Healthy")

        # Big metric cards
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            with st.container(border=True):
                st.metric("Total complaints", len(complaints))
                st.badge("Open: " + str(len(open_c)), color="orange" if open_c else "green")
        with m2:
            with st.container(border=True):
                st.metric("Total incidents", len(incidents))
                st.badge("Active: " + str(len(active_i)), color="red" if active_i else "green")
        with m3:
            with st.container(border=True):
                st.metric("System components", len(health_chk))
                st.badge("Healthy: " + str(healthy), color="green")
        with m4:
            with st.container(border=True):
                resolved = sum(1 for c in complaints if c["status"] in ["Resolved","Closed"])
                st.metric("Resolved complaints", resolved)
                rate = int(resolved / len(complaints) * 100) if complaints else 0
                st.badge(f"Rate: {rate}%", color="green" if rate > 50 else "orange")

        st.space("small")
        # System health quick view
        with st.container(border=True):
            st.markdown("**:material/monitor_heart: System health**")
            if health_chk:
                cols = st.columns(min(len(health_chk), 4))
                for i, h in enumerate(health_chk):
                    color, icon = HEALTH_BADGE.get(h["status"], ("gray",":material/circle:"))
                    with cols[i % 4]:
                        st.markdown(f"**{h['component_name']}**")
                        st.badge(h["status"], icon=icon, color=color)
            else:
                st.caption("No health data available.")

    # ── Tab 1: All Complaints ─────────────────────────────────────────────────
    with tabs[1]:
        st.subheader("All complaints — system-wide")
        res = requests.get(f"{API_URL}/complaints/all", headers=get_headers())
        if res.status_code == 200:
            complaints = res.json()
            if complaints:
                statuses = [c["status"] for c in complaints]
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Total",             len(complaints))
                col_b.metric("Open",              sum(1 for s in statuses if s not in ["Resolved","Closed"]))
                col_c.metric("Resolved / Closed", sum(1 for s in statuses if s in ["Resolved","Closed"]))

                st.space("small")
                all_statuses  = ["All"] + sorted(set(statuses))
                filter_status = st.selectbox("Filter by status", all_statuses, key="admin_complaint_filter")
                filtered      = complaints if filter_status == "All" else [c for c in complaints if c["status"] == filter_status]
                st.caption(f"Showing {len(filtered)} complaint(s)")

                for c in filtered:
                    s_color, s_icon = STATUS_BADGE.get(c["status"],("gray",":material/circle:"))
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
                st.info("No complaints filed yet.", icon=":material/info:")
        else:
            st.error(f"Failed to load complaints. (HTTP {res.status_code})", icon=":material/error:")

    # ── Tab 2: Active Incidents ────────────────────────────────────────────────
    with tabs[2]:
        st.subheader("Active incidents")
        res = requests.get(f"{API_URL}/admin/incidents", headers=get_headers())
        if res.status_code == 200:
            incidents = res.json()
            if incidents:
                st.dataframe(pd.DataFrame(incidents))
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
                        payload = {
                            "incident_reference": ref,
                            "incident_type":      inc_type,
                            "description":        desc,
                            "severity":           severity,
                            "status":             "Detected",
                        }
                        res2 = requests.post(f"{API_URL}/admin/incidents", headers=get_headers(), json=payload)
                        if res2.status_code == 200:
                            st.success("Incident created.", icon=":material/check_circle:")
                            st.rerun()
                        else:
                            st.error(f"Failed: {res2.text}", icon=":material/error:")
                    else:
                        st.warning("Reference and incident type are required.", icon=":material/warning:")

    # ── Tab 3: Response Playbooks ──────────────────────────────────────────────
    with tabs[3]:
        st.subheader(":material/menu_book: Response playbooks")
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
                st.info("No playbooks defined yet.", icon=":material/info:")
        else:
            st.error("Failed to load playbooks.", icon=":material/error:")

    # ── Tab 4: Users ───────────────────────────────────────────────────────────
    with tabs[4]:
        st.subheader(":material/group: User management")
        res = requests.get(f"{API_URL}/admin/users", headers=get_headers())
        if res.status_code == 200:
            users = res.json()
            if users:
                st.dataframe(pd.DataFrame(users))
            else:
                st.info("No users found.", icon=":material/info:")
        else:
            st.error("Failed to load users.", icon=":material/error:")

        st.space("small")
        with st.container(border=True):
            st.markdown("**:material/person_add: Create new user**")
            with st.form("create_user_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    u_name  = st.text_input("Full name",  placeholder="Jane Smith")
                    u_email = st.text_input("Email",      placeholder="jane@org.com")
                with c2:
                    u_phone = st.text_input("Phone",      placeholder="+91…")
                    u_pass  = st.text_input("Password",   type="password", placeholder="••••••••")
                u_role = st.selectbox("Role", ["Victim","Officer","Threat Analyst","Incident Responder","Administrator"])
                if st.form_submit_button("Create user", icon=":material/person_add:", type="primary"):
                    payload = {
                        "full_name":    u_name,
                        "email":        u_email,
                        "phone_number": u_phone,
                        "password":     u_pass,
                        "role_name":    u_role,
                    }
                    res2 = requests.post(f"{API_URL}/admin/users", headers=get_headers(), json=payload)
                    if res2.status_code == 200:
                        st.success("User created.", icon=":material/check_circle:")
                        st.rerun()
                    else:
                        st.error(f"Failed: {res2.text}", icon=":material/error:")

    # ── Tab 5: Roles ───────────────────────────────────────────────────────────
    with tabs[5]:
        st.subheader(":material/badge: Roles & permissions")
        res = requests.get(f"{API_URL}/admin/roles", headers=get_headers())
        if res.status_code == 200:
            roles = res.json()
            if roles:
                st.dataframe(pd.DataFrame(roles))
            else:
                st.info("No roles found.", icon=":material/info:")
        else:
            st.error("Failed to load roles.", icon=":material/error:")

    # ── Tab 6: Audit Logs ─────────────────────────────────────────────────────
    with tabs[6]:
        st.subheader(":material/history: Audit logs")
        res = requests.get(f"{API_URL}/admin/audit-logs", headers=get_headers())
        if res.status_code == 200:
            logs = res.json()
            if logs:
                st.dataframe(pd.DataFrame(logs))
            else:
                st.info("No audit logs available.", icon=":material/info:")
        else:
            st.error("Failed to load audit logs.", icon=":material/error:")

    # ── Tab 7: Login Activity ──────────────────────────────────────────────────
    with tabs[7]:
        st.subheader(":material/login: Login history")
        res = requests.get(f"{API_URL}/admin/login-history", headers=get_headers())
        if res.status_code == 200:
            history = res.json()
            if history:
                st.dataframe(pd.DataFrame(history))
            else:
                st.info("No login history available.", icon=":material/info:")
        else:
            st.error("Failed to load login history.", icon=":material/error:")

    # ── Tab 8: System Health ──────────────────────────────────────────────────
    with tabs[8]:
        st.subheader(":material/monitor_heart: Detailed system health")
        res = requests.get(f"{API_URL}/admin/system-health", headers=get_headers())
        if res.status_code == 200:
            health = res.json()
            if health:
                # Badge view
                cols_h = st.columns(min(len(health), 3))
                for i, h in enumerate(health):
                    color, icon = HEALTH_BADGE.get(h["status"],("gray",":material/circle:"))
                    with cols_h[i % 3]:
                        with st.container(border=True):
                            st.markdown(f"**{h['component_name']}**")
                            st.badge(h["status"], icon=icon, color=color)
                            if h.get("details"):
                                st.caption(h["details"])

                st.space("small")
                st.markdown("**Raw data**")
                st.dataframe(pd.DataFrame(health))
            else:
                st.info("No health records found.", icon=":material/info:")
        else:
            st.error("Failed to load system health.", icon=":material/error:")
