import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"
CHART_TEMPLATE = "plotly_dark"

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

HEALTH_BADGE = {
    "Healthy": ("green",  ":material/check_circle:"),
    "Warning": ("orange", ":material/warning:"),
    "Critical":("red",    ":material/error:"),
}

st.subheader(":material/dashboard: Platform overview")
st.caption("Live summary of complaints, incidents, and system health.")
st.space("small")

# ── Parallel fragments for concurrent loading ──────────────────────────────────

@st.fragment(parallel=True)
def complaints_card():
    with st.container(border=True):
        st.markdown("**:material/list_alt: Complaints**")
        with st.skeleton(height=120):
            res = requests.get(f"{API_URL}/complaints/all", headers=get_headers())
        if res.status_code == 200:
            complaints = res.json()
            open_c     = [c for c in complaints if c["status"] not in ["Resolved","Closed"]]
            resolved   = len(complaints) - len(open_c)
            rate       = int(resolved / len(complaints) * 100) if complaints else 0
            st.metric("Total complaints",  len(complaints))
            st.metric("Open",              len(open_c))
            st.badge(f"Resolution rate: {rate}%", color="green" if rate > 60 else "orange")
        else:
            st.error("Failed to load.", icon=":material/error:")

@st.fragment(parallel=True)
def incidents_card():
    with st.container(border=True):
        st.markdown("**:material/emergency: Incidents**")
        with st.skeleton(height=120):
            res = requests.get(f"{API_URL}/admin/incidents", headers=get_headers())
        if res.status_code == 200:
            incidents = res.json()
            active    = [i for i in incidents if i["status"] not in ["Resolved","Closed"]]
            st.metric("Total incidents", len(incidents))
            st.metric("Active",          len(active))
            if active:
                st.badge(f"{len(active)} active", icon=":material/emergency:", color="red")
            else:
                st.badge("All clear", icon=":material/check_circle:", color="green")
        else:
            st.error("Failed to load.", icon=":material/error:")

@st.fragment(parallel=True)
def health_card():
    with st.container(border=True):
        st.markdown("**:material/monitor_heart: System health**")
        with st.skeleton(height=120):
            res = requests.get(f"{API_URL}/admin/system-health", headers=get_headers())
        if res.status_code == 200:
            health = res.json()
            healthy = sum(1 for h in health if h["status"] == "Healthy")
            st.metric("Total components", len(health))
            st.metric("Healthy",          healthy)
            for h in health:
                color, icon = HEALTH_BADGE.get(h["status"],("gray",":material/circle:"))
                st.badge(h["component_name"], icon=icon, color=color)
        else:
            st.error("Failed to load.", icon=":material/error:")

# Three columns, each with a parallel fragment
c1, c2, c3 = st.columns(3)
with c1: complaints_card()
with c2: incidents_card()
with c3: health_card()

# ── Charts row ────────────────────────────────────────────────────────────────
st.space("small")

@st.fragment(parallel=True)
def complaint_status_chart():
    with st.container(border=True):
        st.markdown("**Complaint status breakdown**")
        with st.skeleton(height=280):
            res = requests.get(f"{API_URL}/complaints/all", headers=get_headers())
        if res.status_code == 200 and res.json():
            complaints = res.json()
            from collections import Counter
            status_counts = Counter(c["status"] for c in complaints)
            df = pd.DataFrame({"status": list(status_counts.keys()), "count": list(status_counts.values())})
            color_map = {
                "Submitted":"#60A5FA","Under Review":"#38BDF8","Assigned":"#A78BFA",
                "Investigation":"#FB923C","Action Taken":"#FBBF24",
                "Resolved":"#34D399","Closed":"#94A3B8",
            }
            fig = px.pie(df, names="status", values="count",
                         color="status", color_discrete_map=color_map,
                         template=CHART_TEMPLATE)
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(showlegend=True, margin=dict(t=10,b=10,l=10,r=10))
            st.plotly_chart(fig)

@st.fragment(parallel=True)
def incident_severity_chart():
    with st.container(border=True):
        st.markdown("**Incident severity breakdown**")
        with st.skeleton(height=280):
            res = requests.get(f"{API_URL}/admin/incidents", headers=get_headers())
        if res.status_code == 200 and res.json():
            incidents = res.json()
            from collections import Counter
            sev_counts = Counter(i.get("severity","Unknown") for i in incidents)
            df = pd.DataFrame({"severity": list(sev_counts.keys()), "count": list(sev_counts.values())})
            color_map = {"Low":"#34D399","Medium":"#FBBF24","High":"#FB923C","Critical":"#F87171","Unknown":"#94A3B8"}
            fig = px.bar(df, x="severity", y="count",
                         color="severity", color_discrete_map=color_map,
                         template=CHART_TEMPLATE)
            fig.update_layout(showlegend=False, margin=dict(t=10,b=10))
            st.plotly_chart(fig)
        elif res.status_code == 200:
            st.info("No incident data yet.", icon=":material/info:")

chart_col1, chart_col2 = st.columns(2)
with chart_col1: complaint_status_chart()
with chart_col2: incident_severity_chart()
