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

st.subheader(":material/trending_up: Threat trends")
st.caption("Distribution of IOCs by type and risk level.")
st.space("small")

with st.skeleton(height=400):
    res = requests.get(f"{API_URL}/threat-trends", headers=get_headers())

if res.status_code == 200:
    data = res.json()
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("**IOCs by type**")
            if data["by_type"]:
                df = pd.DataFrame(data["by_type"])
                fig = px.bar(df, x="ioc_type", y="count", color="ioc_type",
                             color_discrete_sequence=IOC_COLORS, template=CHART_TEMPLATE)
                fig.update_layout(showlegend=False, margin=dict(t=10,b=10))
                st.plotly_chart(fig)
            else:
                st.info("No data.", icon=":material/info:")
    with col2:
        with st.container(border=True):
            st.markdown("**IOCs by risk level**")
            if data["by_risk"]:
                df = pd.DataFrame(data["by_risk"])
                fig = px.bar(df, x="risk_level", y="count", color="risk_level",
                             color_discrete_map=RISK_COLORS, template=CHART_TEMPLATE)
                fig.update_layout(showlegend=False, margin=dict(t=10,b=10))
                st.plotly_chart(fig)
            else:
                st.info("No data.", icon=":material/info:")
else:
    st.error("Failed to load trends.", icon=":material/error:")
