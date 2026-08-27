import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/add_circle: New complaint")
st.caption("Fill in the details below. Fields marked * are required.")
st.space("small")

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
        desc = st.text_area(
            "Description *",
            placeholder="Describe what happened in detail — the more information the better…",
            height=150,
        )
        loss = st.number_input("Financial loss (₹)", min_value=0.0, format="%.2f")

        with st.expander(":material/person_search: Suspect details (optional)"):
            c1, c2, c3 = st.columns(3)
            with c1:
                url = st.text_input("Suspected URL", placeholder="https://…")
            with c2:
                phone = st.text_input("Suspected phone", placeholder="+91…")
            with c3:
                email = st.text_input("Suspected email", placeholder="scammer@…")

        st.space("small")
        submit = st.form_submit_button(
            "Submit complaint",
            icon=":material/send:",
            type="primary",
        )

@st.dialog("Review your complaint")
def confirm_submit(payload):
    st.markdown(f"**Title:** {payload['title']}")
    st.markdown(f"**Category ID:** {payload['category_id']}")
    st.markdown(f"**Incident date:** {payload['incident_date']}")
    st.markdown(f"**Description:** {payload['description'][:200]}{'…' if len(payload['description']) > 200 else ''}")
    st.markdown(f"**Financial loss:** ₹{payload['financial_loss']:,.2f}")
    st.space("small")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Confirm & submit", icon=":material/check:", type="primary"):
            res = requests.post(f"{API_URL}/complaints/", headers=get_headers(), json=payload)
            if res.status_code == 200:
                tracking_id = res.json().get("tracking_id", "N/A")
                st.session_state["complaint_submitted_msg"] = (
                    f"Complaint submitted! Your Tracking ID is **{tracking_id}**. "
                    f"View it under 'My complaints'."
                )
                st.rerun()
            else:
                st.error(f"Submission failed: {res.text}", icon=":material/error:")
    with col2:
        if st.button("Go back & edit", icon=":material/arrow_back:"):
            st.rerun()

if submit:
    if not title or not desc:
        st.error("Title and description are required.", icon=":material/error:")
    else:
        payload = {
            "category_id":    category_id,
            "title":          title,
            "incident_date":  str(incident_date),
            "description":    desc,
            "financial_loss": loss,
            "suspected_url":   url   or None,
            "suspected_phone": phone or None,
            "suspected_email": email or None,
        }
        confirm_submit(payload)
