import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"


def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}


def render():
    st.header("Threat Intelligence Dashboard")

    tabs = st.tabs([
        "Threat Overview", "IOC Search", "Threat Feeds",
        "High-Risk Indicators", "Campaigns", "Threat Trends", "Threat Forecast"
    ])

    # ---- Threat Overview ----
    with tabs[0]:
        st.subheader("Threat Overview")
        trends = requests.get(f"{API_URL}/threat-trends", headers=get_headers())
        if trends.status_code == 200:
            data = trends.json()
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**IOCs by Type**")
                if data["by_type"]:
                    df = pd.DataFrame(data["by_type"])
                    fig = px.pie(df, names="ioc_type", values="count", title="IOC Distribution by Type")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No IOCs registered yet.")
            with col2:
                st.markdown("**IOCs by Risk Level**")
                if data["by_risk"]:
                    df = pd.DataFrame(data["by_risk"])
                    color_map = {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444", "Critical": "#7c3aed"}
                    fig = px.bar(df, x="risk_level", y="count", title="IOC Count by Risk Level",
                                 color="risk_level", color_discrete_map=color_map)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No IOCs registered yet.")
        else:
            st.error("Failed to load threat overview")

    # ---- IOC Search ----
    with tabs[1]:
        st.subheader("Search Indicators of Compromise")
        search_val = st.text_input("Enter indicator value (IP, domain, URL, hash, email)")
        if st.button("Search"):
            if search_val:
                res = requests.get(f"{API_URL}/iocs/search", headers=get_headers(), params={"value": search_val})
                if res.status_code == 200:
                    results = res.json()
                    if results:
                        st.dataframe(pd.DataFrame(results))
                    else:
                        st.warning("No matching IOCs found.")
                else:
                    st.error("Search failed")

        st.divider()
        st.subheader("Register New IOC")
        with st.form("ioc_form"):
            ioc_type = st.selectbox("IOC Type", ["IP", "Domain", "URL", "Hash", "Email"])
            ioc_value = st.text_input("IOC Value")
            risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High", "Critical"])
            submitted = st.form_submit_button("Register IOC")
            if submitted and ioc_value:
                payload = {"ioc_type": ioc_type, "ioc_value": ioc_value, "risk_level": risk_level}
                res = requests.post(f"{API_URL}/iocs", headers=get_headers(), json=payload)
                if res.status_code == 200:
                    st.success(f"IOC registered: {ioc_value}")
                else:
                    st.error(f"Failed: {res.text}")

    # ---- Threat Feeds ----
    with tabs[2]:
        st.subheader("Ingested Threat Feeds")
        res = requests.get(f"{API_URL}/threat-feeds", headers=get_headers())
        if res.status_code == 200:
            feeds = res.json()
            if feeds:
                st.dataframe(pd.DataFrame(feeds))
            else:
                st.info("No threat feeds ingested yet.")
        else:
            st.error("Failed to load feeds")

    # ---- High-Risk Indicators ----
    with tabs[3]:
        st.subheader("High-Risk Indicators (High & Critical)")
        res = requests.get(f"{API_URL}/threats", headers=get_headers())
        if res.status_code == 200:
            threats = res.json()
            if threats:
                st.dataframe(pd.DataFrame(threats))
            else:
                st.info("No high-risk indicators found.")
        else:
            st.error("Failed to load threats")

    # ---- Campaigns ----
    with tabs[4]:
        st.subheader("Detected Campaigns")
        res = requests.get(f"{API_URL}/campaigns", headers=get_headers())
        if res.status_code == 200:
            campaigns = res.json()
            if campaigns:
                for c in campaigns:
                    with st.expander(f"{c['campaign_name']} (Risk: {c['risk_level']})"):
                        st.write(f"**Detected:** {c['detected_at']}")
                        st.write(f"**Description:** {c.get('description', 'N/A')}")
            else:
                st.info("No campaigns detected yet.")
        else:
            st.error("Failed to load campaigns")

    # ---- Threat Trends ----
    with tabs[5]:
        st.subheader("Threat Trends")
        res = requests.get(f"{API_URL}/threat-trends", headers=get_headers())
        if res.status_code == 200:
            data = res.json()
            if data["by_type"]:
                df = pd.DataFrame(data["by_type"])
                fig = px.bar(df, x="ioc_type", y="count", title="IOCs by Type", color="ioc_type")
                st.plotly_chart(fig, use_container_width=True)
            if data["by_risk"]:
                df = pd.DataFrame(data["by_risk"])
                fig = px.bar(df, x="risk_level", y="count", title="IOCs by Risk Level", color="risk_level")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Failed to load trends")

    # ---- Threat Forecast ----
    with tabs[6]:
        st.subheader("Threat Forecast")
        res = requests.get(f"{API_URL}/threat-forecast", headers=get_headers())
        if res.status_code == 200:
            data = res.json()
            col1, col2, col3 = st.columns(3)
            col1.metric("Total IOCs", data["total_iocs"])
            col2.metric("Last 7 Days", data["last_7_days"])
            col3.metric("Last 30 Days", data["last_30_days"])

            col4, col5 = st.columns(2)
            col4.metric("Avg Daily (7d)", data["avg_daily_7d"])
            col5.metric("Avg Daily (30d)", data["avg_daily_30d"])
        else:
            st.error("Failed to load forecast")
