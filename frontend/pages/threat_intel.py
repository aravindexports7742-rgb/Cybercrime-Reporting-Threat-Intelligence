import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:8000"

# Dark-mode Plotly theme
CHART_TEMPLATE = "plotly_dark"
RISK_COLORS = {
    "Low":      "#34D399",
    "Medium":   "#FBBF24",
    "High":     "#FB923C",
    "Critical": "#F87171",
}
IOC_COLORS = ["#60A5FA","#34D399","#A78BFA","#F87171","#FBBF24","#38BDF8"]

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

def render():
    st.subheader(":material/radar: Threat intelligence dashboard")
    st.caption("Monitor indicators of compromise, threat feeds, and campaign trends.")
    st.space("small")

    tabs = st.tabs([
        ":material/dashboard: Overview",
        ":material/search: IOC search",
        ":material/rss_feed: Threat feeds",
        ":material/warning: High-risk IOCs",
        ":material/hub: Campaigns",
        ":material/trending_up: Trends",
        ":material/auto_graph: Forecast",
    ])

    # ── Overview ──────────────────────────────────────────────────────────────
    with tabs[0]:
        st.subheader("Threat overview")
        trends = requests.get(f"{API_URL}/threat-trends", headers=get_headers())
        if trends.status_code == 200:
            data = trends.json()

            # Summary metrics strip
            total_iocs = sum(r["count"] for r in data.get("by_type", []))
            critical   = next((r["count"] for r in data.get("by_risk", []) if r["risk_level"] == "Critical"), 0)
            high       = next((r["count"] for r in data.get("by_risk", []) if r["risk_level"] == "High"), 0)

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                with st.container(border=True):
                    st.metric("Total IOCs", total_iocs)
            with m2:
                with st.container(border=True):
                    st.metric(":red[Critical]", critical)
            with m3:
                with st.container(border=True):
                    st.metric(":orange[High]", high)
            with m4:
                with st.container(border=True):
                    st.metric("IOC types", len(data.get("by_type", [])))

            st.space("small")
            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    st.markdown("**IOC distribution by type**")
                    if data["by_type"]:
                        df = pd.DataFrame(data["by_type"])
                        fig = px.pie(
                            df, names="ioc_type", values="count",
                            color_discrete_sequence=IOC_COLORS,
                            template=CHART_TEMPLATE,
                        )
                        fig.update_traces(textposition="inside", textinfo="percent+label")
                        fig.update_layout(showlegend=True, margin=dict(t=10,b=10,l=10,r=10))
                        st.plotly_chart(fig)
                    else:
                        st.info("No IOCs registered yet.", icon=":material/info:")
            with col2:
                with st.container(border=True):
                    st.markdown("**IOC count by risk level**")
                    if data["by_risk"]:
                        df = pd.DataFrame(data["by_risk"])
                        fig = px.bar(
                            df, x="risk_level", y="count",
                            color="risk_level",
                            color_discrete_map=RISK_COLORS,
                            template=CHART_TEMPLATE,
                        )
                        fig.update_layout(showlegend=False, margin=dict(t=10,b=10,l=10,r=10))
                        st.plotly_chart(fig)
                    else:
                        st.info("No IOCs registered yet.", icon=":material/info:")
        else:
            st.error("Failed to load threat overview.", icon=":material/error:")

    # ── IOC Search ────────────────────────────────────────────────────────────
    with tabs[1]:
        with st.container(border=True):
            st.markdown("**:material/search: Search indicators of compromise**")
            search_val = st.text_input(
                "Indicator value",
                label_visibility="collapsed",
                placeholder="Enter IP, domain, URL, hash, or email…",
            )
            if st.button("Search", icon=":material/search:", type="primary"):
                if search_val:
                    res = requests.get(
                        f"{API_URL}/iocs/search",
                        headers=get_headers(),
                        params={"value": search_val},
                    )
                    if res.status_code == 200:
                        results = res.json()
                        if results:
                            st.dataframe(pd.DataFrame(results), use_container_width=False)
                        else:
                            st.warning("No matching IOCs found.", icon=":material/warning:")
                    else:
                        st.error("Search failed.", icon=":material/error:")

        st.space("small")
        with st.container(border=True):
            st.markdown("**:material/add_circle: Register new IOC**")
            with st.form("ioc_form"):
                c1, c2 = st.columns(2)
                with c1:
                    ioc_type  = st.selectbox("IOC type", ["IP","Domain","URL","Hash","Email"])
                    ioc_value = st.text_input("IOC value", placeholder="e.g. 192.168.1.1")
                with c2:
                    risk_level = st.selectbox("Risk level", ["Low","Medium","High","Critical"])
                submitted = st.form_submit_button("Register IOC", icon=":material/add:", type="primary")
                if submitted and ioc_value:
                    payload = {"ioc_type": ioc_type, "ioc_value": ioc_value, "risk_level": risk_level}
                    res = requests.post(f"{API_URL}/iocs", headers=get_headers(), json=payload)
                    if res.status_code == 200:
                        st.success(f"IOC registered: `{ioc_value}`", icon=":material/check_circle:")
                    else:
                        st.error(f"Failed: {res.text}", icon=":material/error:")

    # ── Threat Feeds ──────────────────────────────────────────────────────────
    with tabs[2]:
        st.subheader("Ingested threat feeds")
        res = requests.get(f"{API_URL}/threat-feeds", headers=get_headers())
        if res.status_code == 200:
            feeds = res.json()
            if feeds:
                st.dataframe(pd.DataFrame(feeds))
            else:
                st.info("No threat feeds ingested yet.", icon=":material/info:")
        else:
            st.error("Failed to load feeds.", icon=":material/error:")

    # ── High-Risk Indicators ──────────────────────────────────────────────────
    with tabs[3]:
        st.subheader("High-risk indicators")
        st.caption("Showing High and Critical severity IOCs only.")
        res = requests.get(f"{API_URL}/threats", headers=get_headers())
        if res.status_code == 200:
            threats = res.json()
            if threats:
                df = pd.DataFrame(threats)
                st.dataframe(df)
            else:
                st.info("No high-risk indicators found.", icon=":material/check_circle:")
        else:
            st.error("Failed to load threats.", icon=":material/error:")

    # ── Campaigns ─────────────────────────────────────────────────────────────
    with tabs[4]:
        st.subheader(":material/hub: Detected campaigns")
        res = requests.get(f"{API_URL}/campaigns", headers=get_headers())
        if res.status_code == 200:
            campaigns = res.json()
            if campaigns:
                for c in campaigns:
                    risk    = c["risk_level"]
                    r_color = {"Low":"green","Medium":"yellow","High":"orange","Critical":"red"}.get(risk,"gray")
                    with st.expander(c["campaign_name"], icon=":material/hub:"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Risk level:**")
                            st.badge(risk, color=r_color)
                        with col2:
                            st.markdown(f"**Detected:** {c['detected_at']}")
                        st.markdown(f"**Description:** {c.get('description','N/A')}")
            else:
                st.info("No campaigns detected yet.", icon=":material/info:")
        else:
            st.error("Failed to load campaigns.", icon=":material/error:")

    # ── Threat Trends ─────────────────────────────────────────────────────────
    with tabs[5]:
        st.subheader("Threat trends")
        res = requests.get(f"{API_URL}/threat-trends", headers=get_headers())
        if res.status_code == 200:
            data = res.json()
            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    st.markdown("**IOCs by type**")
                    if data["by_type"]:
                        df = pd.DataFrame(data["by_type"])
                        fig = px.bar(
                            df, x="ioc_type", y="count",
                            color="ioc_type",
                            color_discrete_sequence=IOC_COLORS,
                            template=CHART_TEMPLATE,
                        )
                        fig.update_layout(showlegend=False, margin=dict(t=10,b=10))
                        st.plotly_chart(fig)
            with col2:
                with st.container(border=True):
                    st.markdown("**IOCs by risk level**")
                    if data["by_risk"]:
                        df = pd.DataFrame(data["by_risk"])
                        fig = px.bar(
                            df, x="risk_level", y="count",
                            color="risk_level",
                            color_discrete_map=RISK_COLORS,
                            template=CHART_TEMPLATE,
                        )
                        fig.update_layout(showlegend=False, margin=dict(t=10,b=10))
                        st.plotly_chart(fig)
        else:
            st.error("Failed to load trends.", icon=":material/error:")

    # ── Threat Forecast ───────────────────────────────────────────────────────
    with tabs[6]:
        st.subheader(":material/auto_graph: Threat forecast")
        res = requests.get(f"{API_URL}/threat-forecast", headers=get_headers())
        if res.status_code == 200:
            data = res.json()
            with st.container(border=True):
                st.markdown("**IOC volume summary**")
                c1, c2, c3 = st.columns(3)
                c1.metric("Total IOCs",    data["total_iocs"])
                c2.metric("Last 7 days",   data["last_7_days"])
                c3.metric("Last 30 days",  data["last_30_days"])

            st.space("small")
            with st.container(border=True):
                st.markdown("**Daily averages**")
                c4, c5 = st.columns(2)
                c4.metric("Avg daily (7d)",  data["avg_daily_7d"])
                c5.metric("Avg daily (30d)", data["avg_daily_30d"])
        else:
            st.error("Failed to load forecast.", icon=":material/error:")
