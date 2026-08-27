import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

# Status badge config
STATUS_BADGE = {
    "Submitted":   ("blue",   ":material/pending:"),
    "Under Review":("blue",   ":material/manage_search:"),
    "Assigned":    ("violet", ":material/assignment_ind:"),
    "Investigation":("orange",":material/search:"),
    "Action Taken":("orange", ":material/gavel:"),
    "Resolved":    ("green",  ":material/check_circle:"),
    "Closed":      ("gray",   ":material/do_not_disturb:"),
}

def status_badge(status: str):
    color, icon = STATUS_BADGE.get(status, ("gray", ":material/circle:"))
    st.badge(status, icon=icon, color=color)

def render():
    st.subheader(":material/shield_person: Victim portal")
    st.caption("Manage your complaints, file new reports, and track updates.")
    st.space("small")

    tab_my, tab_new, tab_notif = st.tabs([
        ":material/folder_open: My complaints",
        ":material/add_circle: New complaint",
        ":material/notifications: Notifications",
    ])

    # ── Tab 1: My Complaints ──────────────────────────────────────────────────
    with tab_my:
        # Persistent success banner after complaint submit
        if st.session_state.get("complaint_submitted_msg"):
            st.success(
                st.session_state.pop("complaint_submitted_msg"),
                icon=":material/check_circle:",
            )

        response = requests.get(f"{API_URL}/complaints/", headers=get_headers())
        if response.status_code == 200:
            complaints = response.json()
            if not complaints:
                st.info(
                    "No complaints filed yet. Use the **New complaint** tab to get started.",
                    icon=":material/info:",
                )
            for c in complaints:
                status = c["status"]
                color, icon = STATUS_BADGE.get(status, ("gray", ":material/circle:"))
                with st.expander(
                    f"{c['tracking_id']} — {c['title']}",
                    icon=icon,
                ):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Tracking ID:** `{c['tracking_id']}`")
                        st.markdown(f"**Incident date:** {c['incident_date']}")
                        st.markdown("**Status:**")
                        status_badge(status)
                    with col2:
                        st.markdown(f"**Financial loss:** ₹{c['financial_loss']:,.2f}")
                        st.markdown(f"**Filed on:** {str(c['created_at'])[:10]}")

                    st.markdown(f"**Description:** {c['description']}")

                    extras = []
                    if c.get("suspected_url"):   extras.append(f"🔗 **URL:** {c['suspected_url']}")
                    if c.get("suspected_phone"): extras.append(f"📞 **Phone:** {c['suspected_phone']}")
                    if c.get("suspected_email"): extras.append(f"📧 **Email:** {c['suspected_email']}")
                    for e in extras:
                        st.markdown(e)

                    st.space("small")
                    with st.container(border=True):
                        st.markdown("**:material/attach_file: Upload evidence**")
                        file = st.file_uploader(
                            "Choose a file",
                            label_visibility="collapsed",
                            key=f"file_{c['complaint_id']}",
                        )
                        if st.button("Upload", icon=":material/upload:", key=f"upload_{c['complaint_id']}"):
                            if file:
                                files = {"file": (file.name, file.getvalue(), file.type)}
                                res = requests.post(
                                    f"{API_URL}/complaints/{c['complaint_id']}/evidence",
                                    headers=get_headers(), files=files,
                                )
                                if res.status_code == 200:
                                    st.success("Evidence uploaded.", icon=":material/check_circle:")
                                else:
                                    st.error(f"Upload failed: {res.text}", icon=":material/error:")
                            else:
                                st.warning("Please select a file first.", icon=":material/warning:")
        else:
            st.error(f"Failed to load complaints. (HTTP {response.status_code})", icon=":material/error:")

    # ── Tab 2: New Complaint ──────────────────────────────────────────────────
    with tab_new:
        st.subheader("File a new complaint")
        with st.container(border=True):
            with st.form("complaint_form", clear_on_submit=True):
                title = st.text_input("Title *", placeholder="Brief summary of the incident")

                cats_res = requests.get(f"{API_URL}/complaints/categories", headers=get_headers())
                if cats_res.status_code == 200:
                    cats = cats_res.json()
                    cat_options = {c["category_name"]: c["category_id"] for c in cats}
                    if cat_options:
                        cat_name    = st.selectbox("Crime category *", list(cat_options.keys()))
                        category_id = cat_options[cat_name]
                    else:
                        st.warning("No categories available. Contact admin.", icon=":material/warning:")
                        category_id = 1
                else:
                    category_id = st.number_input("Category ID", min_value=1, value=1)

                incident_date = st.date_input("Incident date *")
                desc  = st.text_area("Description *", placeholder="Describe what happened in detail…")
                loss  = st.number_input("Financial loss (₹)", min_value=0.0, format="%.2f")

                st.markdown("**Suspect details** *(optional)*")
                c1, c2, c3 = st.columns(3)
                with c1: url   = st.text_input("Suspected URL",   placeholder="https://…")
                with c2: phone = st.text_input("Suspected phone",  placeholder="+91…")
                with c3: email = st.text_input("Suspected email",  placeholder="scammer@…")

                st.space("small")
                submit = st.form_submit_button(
                    "Submit complaint",
                    icon=":material/send:",
                    type="primary",
                )
                if submit:
                    if not title or not desc:
                        st.error("Title and description are required.", icon=":material/error:")
                    else:
                        payload = {
                            "category_id":   category_id,
                            "title":         title,
                            "incident_date": str(incident_date),
                            "description":   desc,
                            "financial_loss": loss,
                            "suspected_url":   url   or None,
                            "suspected_phone": phone or None,
                            "suspected_email": email or None,
                        }
                        res = requests.post(f"{API_URL}/complaints/", headers=get_headers(), json=payload)
                        if res.status_code == 200:
                            tracking_id = res.json().get("tracking_id", "N/A")
                            st.session_state["complaint_submitted_msg"] = (
                                f"Complaint submitted! Tracking ID: **{tracking_id}**. "
                                f"Check the 'My complaints' tab to view it."
                            )
                            st.rerun()
                        else:
                            st.error(f"Submission failed: {res.text}", icon=":material/error:")

    # ── Tab 3: Notifications ──────────────────────────────────────────────────
    with tab_notif:
        st.subheader(":material/notifications: Notifications")
        response = requests.get(f"{API_URL}/complaints/notifications/list", headers=get_headers())
        if response.status_code == 200:
            notes = response.json()
            if not notes:
                st.info(
                    "No notifications yet. You'll be notified when your complaint status changes.",
                    icon=":material/notifications_off:",
                )
            for n in notes:
                is_read = n.get("is_read", False)
                with st.container(border=True):
                    col_icon, col_body = st.columns([1, 10], vertical_alignment="center")
                    with col_icon:
                        st.markdown(
                            ":material/mark_email_unread:" if not is_read else ":material/drafts:"
                        )
                    with col_body:
                        st.markdown(f"**{n['event_type']}** — {n['message']}")
                        st.caption(f":material/schedule: {n['created_at']}")
        else:
            st.error(f"Failed to load notifications. (HTTP {response.status_code})", icon=":material/error:")
