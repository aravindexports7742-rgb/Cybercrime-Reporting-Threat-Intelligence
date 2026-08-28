import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CyberShield Platform",
    page_icon=":material/shield:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state initialisation ──────────────────────────────────────────────
if "token" not in st.session_state:
    st.session_state["token"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None

# ── Auth helpers ──────────────────────────────────────────────────────────────
def login(email, password):
    response = requests.post(
        f"{API_URL}/auth/login",
        data={"username": email, "password": password},
    )
    if response.status_code == 200:
        data = response.json()
        st.session_state["token"] = data["access_token"]
        st.session_state["role"] = data.get("role", "Victim")
        st.toast("Logged in successfully!", icon=":material/check_circle:")
        st.rerun()
    else:
        try:
            detail = response.json().get("detail", "Login failed. Check your credentials.")
        except ValueError:
            detail = "Login failed. Check your credentials."
        st.error(detail, icon=":material/error:")

ROLE_META = {
    "Victim":             {"icon": ":material/shield_person:",          "color": "blue"},
    "Officer":            {"icon": ":material/local_police:",           "color": "orange"},
    "Threat Analyst":     {"icon": ":material/radar:",                  "color": "violet"},
    "Incident Responder": {"icon": ":material/emergency:",              "color": "red"},
    "Administrator":      {"icon": ":material/admin_panel_settings:",   "color": "green"},
}

# ══════════════════════════════════════════════════════════════════════════════
# NOT LOGGED IN — Hero login page
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state["token"] is None:

    # Login-only visual treatment: an abstract SOC backdrop with a readable
    # glass panel. It is scoped to this unauthenticated branch, so the working
    # dashboard keeps its normal dark theme after sign-in.
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #06111f;
            background-image:
                radial-gradient(circle at 12% 18%, rgba(37, 99, 235, .28), transparent 28%),
                radial-gradient(circle at 88% 82%, rgba(14, 165, 233, .20), transparent 30%),
                linear-gradient(rgba(96, 165, 250, .055) 1px, transparent 1px),
                linear-gradient(90deg, rgba(96, 165, 250, .055) 1px, transparent 1px),
                linear-gradient(135deg, #06111f 0%, #0b1b31 48%, #071525 100%);
            background-size: auto, auto, 42px 42px, 42px 42px, auto;
            background-attachment: fixed;
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background:
                linear-gradient(115deg, transparent 0 42%, rgba(56, 189, 248, .045) 42.2%, transparent 42.5%),
                linear-gradient(295deg, transparent 0 64%, rgba(167, 139, 250, .04) 64.2%, transparent 64.5%);
            opacity: .9;
        }

        [data-testid="stHeader"] { background: transparent; }
        .block-container {
            max-width: 1280px;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
        }
        [data-testid="stSidebar"] {
            background: rgba(3, 12, 24, .76);
            border-right: 1px solid rgba(96, 165, 250, .14);
        }

        /* The centered login card reads as frosted glass over the backdrop. */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(8, 24, 43, .78);
            border-color: rgba(125, 211, 252, .23);
            box-shadow: 0 24px 80px rgba(0, 0, 0, .30), 0 0 0 1px rgba(255, 255, 255, .025) inset;
            backdrop-filter: blur(16px);
            padding: .8rem;
        }

        [data-testid="stMarkdownContainer"] h1 {
            font-size: clamp(2.25rem, 4vw, 3.4rem);
            letter-spacing: -.03em;
            text-shadow: 0 0 28px rgba(96, 165, 250, .20);
        }

        [data-testid="stTextInput"] input,
        [data-testid="stSelectbox"] [role="combobox"] {
            min-height: 3rem;
            font-size: 1.02rem;
        }
        [data-testid="stButton"] button,
        [data-testid="stFormSubmitButton"] button {
            min-height: 3rem;
            font-size: 1.02rem;
        }

        @media (max-width: 640px) {
            .stApp { background-size: auto, auto, 28px 28px, 28px 28px, auto; }
            .block-container { padding: 1.5rem 1rem 2rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### :material/shield: CyberShield")
        st.caption("Cybercrime Reporting & Threat Intelligence Platform")
        st.divider()
        st.caption("🔒 All data is encrypted in transit.")
        st.caption("📍 For law enforcement and public use.")

    with st.container(horizontal_alignment="center"):
        st.space("large")
        st.badge("SECURE PLATFORM", icon=":material/verified_user:", color="blue")
        st.title("Cybercrime & Threat Intelligence", text_alignment="center")
        st.caption(
            "Report cybercrime incidents, track your cases, and help analysts protect the digital ecosystem.",
            text_alignment="center",
        )
        st.caption(":material/shield_lock: Trusted reporting • encrypted access • secure case tracking", text_alignment="center")
        st.space("medium")

    col_left, col_main, col_right = st.columns([1, 2, 1])
    with col_main:
        with st.container(border=True):
            tab_login, tab_register = st.tabs([
                ":material/login: Sign in",
                ":material/person_add: Register",
            ])

            with tab_login:
                st.space("small")
                email    = st.text_input("Email address", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                st.space("small")
                if st.button("Sign in", icon=":material/login:", type="primary"):
                    login(email, password)

            with tab_register:
                st.space("small")
                with st.form("register_form", clear_on_submit=True):
                    reg_name  = st.text_input("Full name",     placeholder="Jane Smith")
                    reg_email = st.text_input("Email address", placeholder="you@example.com")
                    reg_phone = st.text_input("Phone number",  placeholder="+91 98765 43210")
                    reg_pass  = st.text_input("Password",      type="password", placeholder="••••••••")
                    reg_role  = st.selectbox(
                        "I am a",
                        ["Victim", "Officer", "Threat Analyst", "Incident Responder", "Administrator"],
                    )
                    st.space("small")
                    if st.form_submit_button("Create account", icon=":material/person_add:", type="primary"):
                        payload = {
                            "full_name":    reg_name,
                            "email":        reg_email,
                            "phone_number": reg_phone,
                            "password":     reg_pass,
                            "role_name":    reg_role,
                        }
                        res = requests.post(f"{API_URL}/auth/register", json=payload)
                        if res.status_code == 200:
                            st.success(res.json().get("message", "Account created successfully."), icon=":material/check_circle:")
                        else:
                            st.error(f"Registration failed: {res.text}", icon=":material/error:")

# ══════════════════════════════════════════════════════════════════════════════
# LOGGED IN — Role-based st.navigation
# ══════════════════════════════════════════════════════════════════════════════
else:
    role = st.session_state["role"]
    meta = ROLE_META.get(role, {"icon": ":material/person:", "color": "gray"})

    @st.fragment(run_every=1)
    def live_clock():
        """Keeps the command-center time current without reloading the page."""
        now = datetime.now(ZoneInfo("Asia/Kolkata"))
        st.caption(now.strftime("%A, %d %B %Y  •  %I:%M:%S %p IST"))

    # Shared dashboard chrome. Keeping this in the app shell gives every role
    # the same visual language while leaving each page free to focus on its
    # own workflow.
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #101510;
            background-image:
                radial-gradient(ellipse at 90% 8%, rgba(20, 184, 166, .16), transparent 25%),
                radial-gradient(ellipse at 7% 88%, rgba(245, 158, 11, .09), transparent 24%),
                linear-gradient(120deg, transparent 0 47%, rgba(45, 212, 191, .035) 47.1%, transparent 47.3%),
                linear-gradient(rgba(148, 163, 184, .025) 1px, transparent 1px),
                linear-gradient(90deg, rgba(148, 163, 184, .025) 1px, transparent 1px),
                linear-gradient(135deg, #101510 0%, #121b1b 50%, #0d1415 100%);
            background-size: auto, auto, auto, 56px 56px, 56px 56px, auto;
            background-attachment: fixed;
        }
        .block-container {
            max-width: 1760px;
            padding-top: 2rem;
            padding-bottom: 3rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }
        [data-testid="stHeader"] { background: rgba(16, 21, 16, .76); }
        [data-testid="stSidebar"] {
            background: rgba(12, 18, 18, .90);
            border-right: 1px solid rgba(45, 212, 191, .16);
        }
        [data-testid="stSidebarNav"] { padding-top: .65rem; }
        [data-testid="stSidebarNav"] li a {
            border-radius: 9px;
            margin: 2px 8px;
            transition: background .2s ease, transform .2s ease;
        }
        [data-testid="stSidebarNav"] li a:hover {
            background: rgba(45, 212, 191, .11);
            transform: translateX(2px);
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: linear-gradient(145deg, rgba(24, 38, 38, .86), rgba(13, 24, 25, .80));
            border-color: rgba(94, 234, 212, .15);
            box-shadow: 0 14px 38px rgba(0, 0, 0, .16), 0 0 0 1px rgba(255, 255, 255, .018) inset;
            backdrop-filter: blur(12px);
            padding: .9rem;
        }
        [data-testid="stMetric"] {
            background: rgba(22, 38, 39, .66);
            border: 1px solid rgba(94, 234, 212, .11);
            border-radius: 10px;
            padding: 12px 14px;
        }
        [data-testid="stMetricValue"] {
            letter-spacing: -.04em;
            font-size: 2rem;
        }
        [data-testid="stMetricLabel"] { font-size: .95rem; }
        [data-testid="stExpander"] {
            border-color: rgba(94, 234, 212, .13);
            background: rgba(14, 29, 30, .55);
            border-radius: 10px;
        }
        [data-testid="stMarkdownContainer"] h2 { font-size: 1.75rem; }
        [data-testid="stMarkdownContainer"] h3 { font-size: 1.35rem; }
        [data-testid="stCaptionContainer"] { font-size: .95rem; }
        @media (max-width: 900px) {
            .block-container { padding-left: 1.5rem; padding-right: 1.5rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Build pages list dynamically based on role
    if role == "Victim":
        pages = {
            "My Portal": [
                st.Page("app_pages/victim_complaints.py",      title="My complaints",    icon=":material/folder_open:"),
                st.Page("app_pages/victim_new_complaint.py",   title="New complaint",    icon=":material/add_circle:"),
                st.Page("app_pages/victim_notifications.py",   title="Notifications",    icon=":material/notifications:"),
            ]
        }
    elif role == "Officer":
        pages = {
            "Case Management": [
                st.Page("app_pages/officer_cases.py",      title="Active cases",         icon=":material/folder_open:"),
                st.Page("app_pages/officer_complaints.py", title="All complaints",        icon=":material/list_alt:"),
                st.Page("app_pages/officer_suspects.py",   title="Suspects",              icon=":material/person_search:"),
                st.Page("app_pages/officer_coord.py",      title="Agency coordination",   icon=":material/handshake:"),
            ]
        }
    elif role == "Threat Analyst":
        pages = {
            "Threat Intelligence": [
                st.Page("app_pages/ti_overview.py",     title="Overview",            icon=":material/dashboard:"),
                st.Page("app_pages/ti_ioc_search.py",   title="IOC search",          icon=":material/search:"),
                st.Page("app_pages/ti_feeds.py",        title="Threat feeds",        icon=":material/rss_feed:"),
                st.Page("app_pages/ti_highrisk.py",     title="High-risk IOCs",      icon=":material/warning:"),
                st.Page("app_pages/ti_campaigns.py",    title="Campaigns",           icon=":material/hub:"),
                st.Page("app_pages/ti_trends.py",       title="Trends",              icon=":material/trending_up:"),
                st.Page("app_pages/ti_forecast.py",     title="Forecast",            icon=":material/auto_graph:"),
            ]
        }
    else:  # Administrator / Incident Responder
        pages = {
            "Operations": [
                st.Page("app_pages/admin_overview.py",   title="Overview",            icon=":material/dashboard:"),
                st.Page("app_pages/admin_complaints.py", title="All complaints",       icon=":material/list_alt:"),
                st.Page("app_pages/admin_incidents.py",  title="Active incidents",     icon=":material/emergency:"),
                st.Page("app_pages/admin_playbooks.py",  title="Playbooks",            icon=":material/menu_book:"),
            ],
            "Administration": [
                st.Page("app_pages/admin_users.py",      title="Users",               icon=":material/group:"),
                st.Page("app_pages/admin_roles.py",      title="Roles",               icon=":material/badge:"),
                st.Page("app_pages/admin_audit.py",      title="Audit logs",          icon=":material/history:"),
                st.Page("app_pages/admin_login.py",      title="Login activity",      icon=":material/login:"),
                st.Page("app_pages/admin_health.py",     title="System health",       icon=":material/monitor_heart:"),
            ],
        }

    pg = st.navigation(pages, position="sidebar")

    # Sidebar shared elements
    with st.sidebar:
        st.markdown("### :material/shield: CyberShield")
        st.caption("Operations workspace")
        st.divider()
        st.markdown("**Signed in as**")
        st.badge(role, icon=meta["icon"], color=meta["color"])
        st.space("small")
        if st.button("Sign out", icon=":material/logout:", type="secondary"):
            st.session_state["token"] = None
            st.session_state["role"]  = None
            st.toast("Signed out.", icon=":material/logout:")
            st.rerun()
        st.divider()
        st.caption("CyberShield v1.0 • Secure")

    with st.container(horizontal=True, vertical_alignment="center"):
        with st.container():
            st.markdown("### :material/radar: CyberShield command center")
            st.caption("Monitor reports, coordinate response, and turn intelligence into action.")
            live_clock()
        st.badge(role, icon=meta["icon"], color=meta["color"])

    pg.run()
