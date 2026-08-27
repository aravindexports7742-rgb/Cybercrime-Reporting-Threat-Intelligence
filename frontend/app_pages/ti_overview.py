import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"
CHART_TEMPLATE = "plotly_dark"
RISK_COLORS = {"Low":"#34D399","Medium":"#FBBF24","High":"#FB923C","Critical":"#F87171"}
IOC_COLORS  = ["#60A5FA","#34D399","#A78BFA","#F87171","#FBBF24","#38BDF8"]

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

st.subheader(":material/dashboard: Threat overview")
st.caption("Live summary of indicators of compromise across the platform.")

# Auto-refresh fragment — reruns every 30s without reloading the full page
@st.fragment(run_every=30)
def live_overview():
    trends = requests.get(f"{API_URL}/threat-trends", headers=get_headers())
    if trends.status_code != 200:
        st.error("Failed to load threat overview.", icon=":material/error:")
        return
    data = trends.json()

    total_iocs = sum(r["count"] for r in data.get("by_type", []))
    critical   = next((r["count"] for r in data.get("by_risk", []) if r["risk_level"] == "Critical"), 0)
    high       = next((r["count"] for r in data.get("by_risk", []) if r["risk_level"] == "High"), 0)
    types_cnt  = len(data.get("by_type", []))

    st.space("small")
    with st.container(horizontal=True):
        st.metric("Total IOCs",  total_iocs, border=True)
        st.metric(":red[Critical]", critical, border=True)
        st.metric(":orange[High]",  high,     border=True)
        st.metric("IOC types",   types_cnt,   border=True)

    st.space("small")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("**IOC distribution by type**")
            if data["by_type"]:
                df = pd.DataFrame(data["by_type"])
                fig = px.pie(df, names="ioc_type", values="count",
                             color_discrete_sequence=IOC_COLORS, template=CHART_TEMPLATE)
                fig.update_traces(textposition="inside", textinfo="percent+label")
                fig.update_layout(showlegend=True, margin=dict(t=10,b=10,l=10,r=10))
                st.plotly_chart(fig)
            else:
                st.info("No IOC data yet.", icon=":material/info:")

    with col2:
        with st.container(border=True):
            st.markdown("**IOC count by risk level**")
            if data["by_risk"]:
                df = pd.DataFrame(data["by_risk"])
                fig = px.bar(df, x="risk_level", y="count",
                             color="risk_level", color_discrete_map=RISK_COLORS,
                             template=CHART_TEMPLATE)
                fig.update_layout(showlegend=False, margin=dict(t=10,b=10,l=10,r=10))
                st.plotly_chart(fig)
            else:
                st.info("No IOC data yet.", icon=":material/info:")

    st.caption(":material/refresh: Auto-refreshes every 30 seconds")

live_overview()
