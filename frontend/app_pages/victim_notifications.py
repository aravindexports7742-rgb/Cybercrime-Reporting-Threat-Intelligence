import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

# Fetch notifications
response = requests.get(f"{API_URL}/complaints/notifications/list", headers=get_headers())
notes = response.json() if response.status_code == 200 else []

unread = [n for n in notes if not n.get("is_read", False)]

st.subheader(f":material/notifications: Notifications")
if unread:
    st.badge(f"{len(unread)} unread", icon=":material/mark_email_unread:", color="red")
else:
    st.badge("All read", icon=":material/done_all:", color="green")

st.caption("You'll be notified here whenever your complaint status changes.")
st.space("small")

if not notes:
    with st.container(border=True):
        with st.container(horizontal_alignment="center"):
            st.markdown(":material/notifications_off:")
            st.markdown("**No notifications yet**")
            st.caption("Updates will appear here as your complaint progresses.")
else:
    # Filter
    filter_val = st.segmented_control(
        "Show", ["All", "Unread", "Read"], default="All", key="notif_filter"
    )
    if filter_val == "Unread":
        display = unread
    elif filter_val == "Read":
        display = [n for n in notes if n.get("is_read", False)]
    else:
        display = notes

    for n in display:
        is_read = n.get("is_read", False)
        with st.container(border=True):
            col_icon, col_body = st.columns([1, 12], vertical_alignment="center")
            with col_icon:
                if is_read:
                    st.markdown(":material/drafts:")
                else:
                    st.markdown(":material/mark_email_unread:")
            with col_body:
                if not is_read:
                    st.badge("New", color="blue")
                st.markdown(f"**{n['event_type']}** — {n['message']}")
                st.caption(f":material/schedule: {n['created_at']}")
