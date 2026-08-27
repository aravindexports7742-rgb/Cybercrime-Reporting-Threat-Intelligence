import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

def render():
    st.markdown("<h2>🛡️ Victim Portal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; font-size: 1.1rem; margin-bottom: 1.5rem;'>Manage your complaints, file new reports, and track updates.</p>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 My Complaints", "➕ New Complaint", "🔔 Notifications"])

    # ── Tab 1: My Complaints ──────────────────────────────────────────────────
    with tab1:
        st.subheader("My Complaints")

        # Show persistent success banner if a complaint was just submitted (survives rerun)
        if st.session_state.get("complaint_submitted_msg"):
            st.success(st.session_state.pop("complaint_submitted_msg"))

        response = requests.get(f"{API_URL}/complaints/", headers=get_headers())
        if response.status_code == 200:
            complaints = response.json()
            if not complaints:
                st.info("No complaints filed yet. Use the '➕ New Complaint' tab to get started.")
            for c in complaints:
                status_emoji = {
                    "Submitted": "🟡", "Under Review": "🔵", "Assigned": "🟣",
                    "Investigation": "🔍", "Action Taken": "🟠", "Resolved": "✅", "Closed": "⚫"
                }.get(c["status"], "⚪")
                with st.expander(f"{status_emoji} {c['tracking_id']} — {c['title']} | Status: {c['status']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Tracking ID:** `{c['tracking_id']}`")
                        st.write(f"**Incident Date:** {c['incident_date']}")
                        st.write(f"**Status:** {c['status']}")
                    with col2:
                        st.write(f"**Financial Loss:** ₹{c['financial_loss']}")
                        st.write(f"**Filed On:** {str(c['created_at'])[:10]}")
                    st.write(f"**Description:** {c['description']}")
                    if c.get("suspected_url"):
                        st.write(f"**Suspected URL:** {c['suspected_url']}")
                    if c.get("suspected_phone"):
                        st.write(f"**Suspected Phone:** {c['suspected_phone']}")
                    if c.get("suspected_email"):
                        st.write(f"**Suspected Email:** {c['suspected_email']}")

                    st.markdown("---")
                    st.subheader("📎 Upload Evidence")
                    file = st.file_uploader("Choose file", key=f"file_{c['complaint_id']}")
                    if st.button("Upload", key=f"upload_{c['complaint_id']}"):
                        if file:
                            files = {"file": (file.name, file.getvalue(), file.type)}
                            res = requests.post(
                                f"{API_URL}/complaints/{c['complaint_id']}/evidence",
                                headers=get_headers(), files=files
                            )
                            if res.status_code == 200:
                                st.success("✅ Evidence uploaded successfully!")
                            else:
                                st.error(f"Upload failed: {res.text}")
                        else:
                            st.warning("Please select a file first.")
        else:
            st.error(f"Failed to load complaints. (HTTP {response.status_code})")

    # ── Tab 2: New Complaint ──────────────────────────────────────────────────
    with tab2:
        st.subheader("File a New Complaint")
        with st.form("complaint_form", clear_on_submit=True):
            title = st.text_input("Title *")

            # Fetch categories from backend
            cats_res = requests.get(f"{API_URL}/complaints/categories", headers=get_headers())
            if cats_res.status_code == 200:
                cats = cats_res.json()
                cat_options = {c["category_name"]: c["category_id"] for c in cats}
                if cat_options:
                    cat_name = st.selectbox("Crime Category *", list(cat_options.keys()))
                    category_id = cat_options[cat_name]
                else:
                    st.warning("No categories available. Please contact admin.")
                    category_id = 1
            else:
                category_id = st.number_input("Category ID", min_value=1, value=1)

            incident_date = st.date_input("Incident Date *")
            desc = st.text_area("Description *")
            loss = st.number_input("Financial Loss (₹)", min_value=0.0, format="%.2f")
            url = st.text_input("Suspected URL (optional)")
            phone = st.text_input("Suspected Phone (optional)")
            email = st.text_input("Suspected Email (optional)")

            submit = st.form_submit_button("🚨 Submit Complaint")
            if submit:
                if not title or not desc:
                    st.error("Title and Description are required fields.")
                else:
                    payload = {
                        "category_id": category_id,
                        "title": title,
                        "incident_date": str(incident_date),
                        "description": desc,
                        "financial_loss": loss,
                        "suspected_url": url or None,
                        "suspected_phone": phone or None,
                        "suspected_email": email or None,
                    }
                    res = requests.post(f"{API_URL}/complaints/", headers=get_headers(), json=payload)
                    if res.status_code == 200:
                        tracking_id = res.json().get("tracking_id", "N/A")
                        # Store message in session_state so it survives st.rerun()
                        st.session_state["complaint_submitted_msg"] = (
                            f"✅ Complaint submitted! Your Tracking ID is **{tracking_id}**. "
                            f"Check the '📋 My Complaints' tab to view it."
                        )
                        st.rerun()
                    else:
                        st.error(f"Submission failed: {res.text}")

    # ── Tab 3: Notifications ──────────────────────────────────────────────────
    with tab3:
        st.subheader("🔔 Notifications")
        response = requests.get(f"{API_URL}/complaints/notifications/list", headers=get_headers())
        if response.status_code == 200:
            notes = response.json()
            if not notes:
                st.info("No notifications yet. You'll be notified here when your complaint status changes.")
            for n in notes:
                icon = "📩" if not n.get("is_read") else "📭"
                st.markdown(
                    f"{icon} **{n['event_type']}** — {n['message']}  \n"
                    f"<small>🕐 {n['created_at']}</small>",
                    unsafe_allow_html=True
                )
                st.divider()
        else:
            st.error(f"Failed to load notifications. (HTTP {response.status_code})")
