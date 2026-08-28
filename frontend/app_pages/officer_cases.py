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
    "New":                      ("blue",   ":material/fiber_new:"),
    "Under Review":             ("blue",   ":material/manage_search:"),
    "Assigned":                 ("violet", ":material/assignment_ind:"),
    "Investigation":            ("orange", ":material/search:"),
    "Pending External Response":("yellow", ":material/hourglass_empty:"),
    "Action Taken":             ("orange", ":material/gavel:"),
    "Resolved":                 ("green",  ":material/check_circle:"),
    "Closed":                   ("gray",   ":material/do_not_disturb:"),
}

st.subheader(":material/folder_open: Active cases")
st.caption("Manage, update priority, and add investigation notes to assigned cases.")
st.space("small")

with st.skeleton(height=500):
    response = requests.get(f"{API_URL}/cases/", headers=get_headers())

if response.status_code == 200:
    cases = response.json()
    if not cases:
        with st.container(border=True):
            with st.container(horizontal_alignment="center"):
                st.markdown(":material/folder_open:")
                st.markdown("**No cases found**")
                st.caption("Cases are automatically created when victims submit complaints.")
    else:
        # Summary metrics with sparklines (counts by priority)
        pri_counts = {p: sum(1 for c in cases if c["priority"] == p) for p in ["Low","Medium","High","Critical"]}
        with st.container(horizontal=True):
            st.metric("Total cases",       len(cases),              border=True)
            st.metric(":green[Low]",       pri_counts["Low"],       border=True)
            st.metric(":yellow[Medium]",   pri_counts["Medium"],    border=True)
            st.metric(":orange[High]",     pri_counts["High"],      border=True)
            st.metric(":red[Critical]",    pri_counts["Critical"],  border=True)

        st.space("small")

        # Priority filter
        pri_filter = st.segmented_control(
            "Filter by priority",
            ["All", "Low", "Medium", "High", "Critical"],
            default="All",
            key="officer_pri_filter",
        )
        filtered = cases if pri_filter == "All" else [c for c in cases if c["priority"] == pri_filter]
        st.caption(f"Showing {len(filtered)} case(s)")
        st.space("small")

        for c in filtered:
            pri                  = c["priority"]
            p_color, p_icon      = PRIORITY_BADGE.get(pri, ("gray", ":material/circle:"))
            s_color, s_icon      = STATUS_BADGE.get(c["status"], ("gray", ":material/circle:"))

            with st.expander(f"{c['case_reference']} — {c['status']}", icon=p_icon):
                # Metric strip
                m1, m2, m3 = st.columns(3)
                with m1:
                    with st.container(border=True):
                        st.caption("Case ID"); st.markdown(f"`{c['case_id']}`")
                with m2:
                    with st.container(border=True):
                        st.caption("Priority"); st.badge(pri, icon=p_icon, color=p_color)
                with m3:
                    with st.container(border=True):
                        st.caption("Opened"); st.markdown(str(c["opened_at"])[:10])

                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.markdown("**Status:**"); st.badge(c["status"], icon=s_icon, color=s_color)
                with col_info2:
                    st.markdown(f"**Linked complaint:** {c.get('complaint_id','N/A')}")
                    if c.get("lead_officer_id"):
                        st.markdown(f"**Lead officer:** {c['lead_officer_id']}")

                st.space("small")
                with st.container(border=True):
                    st.markdown("**:material/edit: Update case**")
                    col_s, col_p = st.columns(2)
                    statuses   = ["New","Under Review","Assigned","Investigation","Pending External Response","Action Taken","Resolved","Closed"]
                    priorities = ["Low","Medium","High","Critical"]
                    with col_s:
                        new_status = st.selectbox("Status", statuses,
                            index=statuses.index(c["status"]), key=f"status_{c['case_id']}")
                    with col_p:
                        new_priority = st.selectbox("Priority", priorities,
                            index=priorities.index(c["priority"]), key=f"priority_{c['case_id']}")
                    if st.button("Save changes", icon=":material/save:", key=f"save_{c['case_id']}", type="primary"):
                        res = requests.put(
                            f"{API_URL}/cases/{c['case_id']}",
                            headers=get_headers(),
                            json={"status": new_status, "priority": new_priority},
                        )
                        if res.status_code == 200:
                            st.toast("Case updated!", icon=":material/check_circle:")
                            st.rerun()
                        else:
                            st.error(f"Update failed: {res.text}", icon=":material/error:")

                with st.container(border=True):
                    st.markdown("**:material/edit_note: Investigation notes**")
                    note_text = st.text_area(
                        "Add a note", label_visibility="collapsed",
                        placeholder="Enter investigation notes…", key=f"note_{c['case_id']}",
                    )
                    if st.button("Add note", icon=":material/add:", key=f"add_note_{c['case_id']}"):
                        if note_text:
                            res = requests.post(
                                f"{API_URL}/cases/{c['case_id']}/investigations",
                                headers=get_headers(), json={"note_text": note_text},
                            )
                            if res.status_code == 200:
                                st.toast("Note added.", icon=":material/check_circle:")
                                st.rerun()
                            else:
                                st.error(f"Failed: {res.text}", icon=":material/error:")
                        else:
                            st.warning("Note cannot be empty.", icon=":material/warning:")

                with st.container(border=True):
                    st.markdown("**:material/task_alt: Investigation activity & outcome**")
                    st.caption("Record the concrete work completed and its result. This becomes the case progress history.")
                    with st.form(f"activity_form_{c['case_id']}", clear_on_submit=True):
                        action = st.text_input("Action completed", placeholder="Requested bank account freeze")
                        result = st.text_area("Result / next step", placeholder="Request sent; awaiting the bank response.")
                        saved = st.form_submit_button("Record activity", icon=":material/add_task:")
                    if saved:
                        if not action.strip():
                            st.warning("Action completed is required.", icon=":material/warning:")
                        else:
                            res = requests.post(
                                f"{API_URL}/cases/{c['case_id']}/activities",
                                headers=get_headers(), json={"action": action.strip(), "result": result.strip() or None},
                            )
                            if res.status_code == 200:
                                st.toast("Investigation activity recorded.", icon=":material/check_circle:")
                                st.rerun()
                            else:
                                st.error(f"Could not record activity: {res.text}", icon=":material/error:")

                    activities_res = requests.get(f"{API_URL}/cases/{c['case_id']}/activities", headers=get_headers())
                    if activities_res.status_code == 200:
                        activities = activities_res.json()
                        if activities:
                            st.markdown("**Progress history**")
                            for item in activities:
                                st.markdown(f"- **{str(item['activity_date'])[:16]}** — {item['action']}")
                                if item.get("result"):
                                    st.caption(f"Outcome: {item['result']}")
                        else:
                            st.caption("No activity has been recorded yet.")
else:
    st.error(f"Failed to load cases. (HTTP {response.status_code})", icon=":material/error:")
