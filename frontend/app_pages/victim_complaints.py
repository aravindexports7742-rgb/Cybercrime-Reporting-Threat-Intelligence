import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

STATUS_ORDER = ["Submitted", "Under Review", "Assigned", "Investigation", "Action Taken", "Resolved", "Closed"]
STATUS_BADGE = {
    "Submitted":    ("blue",   ":material/pending:"),
    "Under Review": ("blue",   ":material/manage_search:"),
    "Assigned":     ("violet", ":material/assignment_ind:"),
    "Investigation":("orange", ":material/search:"),
    "Action Taken": ("orange", ":material/gavel:"),
    "Resolved":     ("green",  ":material/check_circle:"),
    "Closed":       ("gray",   ":material/do_not_disturb:"),
}

def complaint_timeline(current_status: str):
    """Renders a horizontal step-by-step progress tracker."""
    steps = STATUS_ORDER
    try:
        current_idx = steps.index(current_status)
    except ValueError:
        current_idx = 0

    # Build HTML stepper
    items = []
    for i, s in enumerate(steps):
        if i < current_idx:
            color = "#34D399"; icon = "✓"
        elif i == current_idx:
            color = "#60A5FA"; icon = "●"
        else:
            color = "#334155"; icon = "○"
        items.append(
            f'<div style="display:flex;flex-direction:column;align-items:center;flex:1;min-width:0;">'
            f'  <div style="width:28px;height:28px;border-radius:50%;background:{color};'
            f'              display:flex;align-items:center;justify-content:center;'
            f'              font-size:13px;color:#fff;font-weight:700;">{icon}</div>'
            f'  <span style="font-size:10px;color:{"#F1F5F9" if i <= current_idx else "#64748B"};'
            f'               margin-top:4px;text-align:center;word-break:break-word;">{s}</span>'
            f'</div>'
        )
        if i < len(steps) - 1:
            line_color = "#34D399" if i < current_idx else "#334155"
            items.append(
                f'<div style="flex:0 0 24px;height:2px;background:{line_color};'
                f'            margin-top:14px;align-self:flex-start;margin-left:-2px;margin-right:-2px;"></div>'
            )

    html = (
        '<div style="display:flex;align-items:flex-start;padding:12px 4px;overflow-x:auto;">'
        + "".join(items)
        + "</div>"
    )
    st.html(html)

# ── Show persistent submission success ────────────────────────────────────────
if st.session_state.get("complaint_submitted_msg"):
    st.success(st.session_state.pop("complaint_submitted_msg"), icon=":material/check_circle:")

st.subheader(":material/folder_open: My complaints")
st.caption("All complaints you have filed, with real-time status tracking.")
st.space("small")

with st.skeleton(height=400):
    response = requests.get(f"{API_URL}/complaints/", headers=get_headers())

if response.status_code == 200:
    complaints = response.json()
    if not complaints:
        with st.container(border=True):
            with st.container(horizontal_alignment="center"):
                st.markdown(":material/folder_open:")
                st.markdown("**No complaints yet**")
                st.caption("Use **New complaint** in the sidebar to file your first report.")
    else:
        # Summary strip
        total     = len(complaints)
        resolved  = sum(1 for c in complaints if c["status"] in ["Resolved","Closed"])
        open_c    = total - resolved
        with st.container(horizontal=True):
            st.metric("Total filed",       total,    border=True)
            st.metric("Open",              open_c,   border=True)
            st.metric("Resolved / Closed", resolved, border=True)

        st.space("small")

        # Status filter
        all_statuses   = ["All"] + sorted({c["status"] for c in complaints})
        status_filter  = st.segmented_control(
            "Filter by status", all_statuses, default="All", key="victim_status_filter"
        )
        filtered = complaints if status_filter == "All" else [c for c in complaints if c["status"] == status_filter]
        st.caption(f"Showing {len(filtered)} complaint(s)")
        st.space("small")

        for c in filtered:
            status            = c["status"]
            badge_color, icon = STATUS_BADGE.get(status, ("gray", ":material/circle:"))
            with st.expander(f"`{c['tracking_id']}` — {c['title']}", icon=icon):
                # Status timeline
                with st.container(border=True):
                    st.caption("Case progress")
                    complaint_timeline(status)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Tracking ID:** `{c['tracking_id']}`")
                    st.markdown(f"**Incident date:** {c['incident_date']}")
                    st.markdown("**Status:**")
                    st.badge(status, icon=icon, color=badge_color)
                with col2:
                    st.markdown(f"**Financial loss:** ₹{c['financial_loss']:,.2f}")
                    st.markdown(f"**Filed on:** {str(c['created_at'])[:10]}")

                st.markdown(f"**Description:** {c['description']}")
                for label, key in [
                    ("Suspected URL",   "suspected_url"),
                    ("Suspected phone", "suspected_phone"),
                    ("Suspected email", "suspected_email"),
                ]:
                    if c.get(key):
                        st.markdown(f"**{label}:** {c[key]}")

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
                            with st.status("Uploading evidence…", expanded=True) as upload_status:
                                st.write("Sending to server…")
                                files = {"file": (file.name, file.getvalue(), file.type)}
                                res = requests.post(
                                    f"{API_URL}/complaints/{c['complaint_id']}/evidence",
                                    headers=get_headers(), files=files,
                                )
                                if res.status_code == 200:
                                    upload_status.update(label="Evidence uploaded!", state="complete")
                                else:
                                    upload_status.update(label=f"Upload failed: {res.text}", state="error")
                        else:
                            st.warning("Please select a file first.", icon=":material/warning:")
else:
    st.error(f"Failed to load complaints. (HTTP {response.status_code})", icon=":material/error:")
