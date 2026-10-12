import base64
import mysql.connector
import pandas as pd
import plotly.express as px
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Solar Energy ERP Analytics Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session State Navigation Logic 
if "view_dashboard" not in st.session_state:
    st.session_state.view_dashboard = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "Operational Metrics"


def go_to_dashboard():
    st.session_state.view_dashboard = True


def go_to_home():
    st.session_state.view_dashboard = False


# Database Connection Helper 
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_PASSWORD_HERE",
        port=3306,
        database="solar_erp",
        use_pure=True,
    )


# Helper Function for White Plotly Styling 
def apply_white_theme(fig):
    """Applies pure white text styling safely across all chart types."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF", size=12),
        title_font=dict(color="#FFFFFF", size=16),
        legend=dict(
            font=dict(color="#FFFFFF"), title_font=dict(color="#FFFFFF")
        ),
        xaxis=dict(
            title=dict(font=dict(color="#FFFFFF")),
            tickfont=dict(color="#FFFFFF"),
            showgrid=False,
        ),
        yaxis=dict(
            title=dict(font=dict(color="#FFFFFF")),
            tickfont=dict(color="#FFFFFF"),
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)",
        ),
        coloraxis_colorbar=dict(
            title=dict(font=dict(color="#FFFFFF")),
            tickfont=dict(color="#FFFFFF"),
        ),
    )

    fig.update_traces(
        textfont=dict(color="#FFFFFF"), selector=dict(type="bar")
    )
    fig.update_traces(
        textfont=dict(color="#FFFFFF"), selector=dict(type="scatter")
    )
    fig.update_traces(
        textfont=dict(color="#FFFFFF"), selector=dict(type="pie")
    )

    return fig


# Background Image Encoding 
try:
    with open("new.png", "rb") as f:
        img = base64.b64encode(f.read()).decode()
    bg_style = f"""
    .stApp {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    """
except Exception:
    bg_style = ".stApp { background-color: #0F172A; }"

# Dynamic Sidebar Hiding CSS
if not st.session_state.view_dashboard:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Global Styling 
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');

    {bg_style}

    .material-symbols-outlined {{
        font-family: 'Material Symbols Outlined' !important;
        font-weight: normal;
        font-style: normal;
        font-size: 22px;
        display: inline-block;
        line-height: 1;
        text-transform: none;
        letter-spacing: normal;
        word-wrap: normal;
        white-space: nowrap;
        direction: ltr;
        vertical-align: middle;
        margin-right: 6px;
    }}

    .dashboard-title-container {{
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 5px;
        margin-bottom: 20px;
    }}

    .title-icon-box {{
        width: 48px;
        height: 48px;
        background: rgba(0, 242, 254, 0.15);
        border: 1px solid rgba(0, 242, 254, 0.5);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2);
    }}

    .main-title-text {{
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 50%, #FFFFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 34px !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        margin: 0 !important;
        filter: drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.9));
    }}

    .stApp h3 {{
        color: #FFFFFF !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        padding-left: 12px;
        border-left: 4px solid #00F2FE;
        margin-top: 25px !important;
        margin-bottom: 15px !important;
        letter-spacing: 0.5px;
    }}

    .stApp, .stApp p, .stApp span, .stApp div, .stApp label {{
        color: #FFFFFF !important;
    }}

    /* Selectbox Text Override */
    div[data-baseweb="select"] * {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }}

    div[data-baseweb="popover"] * {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }}

    .hero-card {{
        background: rgba(15, 23, 42, 0.82);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 242, 254, 0.25);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }}

    .feature-card {{
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 12px;
        padding: 18px;
        height: 100%;
        transition: transform 0.3s ease;
    }}

    .feature-card:hover {{
        transform: translateY(-5px);
        border-color: #00F2FE;
    }}

    .feature-title {{
        font-size: 16px;
        font-weight: 700;
        color: #00F2FE;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
    }}

    /* Standard Button Styling */
    div.stButton > button {{
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(0, 242, 254, 0.4) !important;
        color: #FFFFFF !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 10px 18px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease-in-out !important;
    }}

    div.stButton > button:hover {{
        background: rgba(0, 242, 254, 0.2) !important;
        border-color: #00F2FE !important;
        color: #00F2FE !important;
        box-shadow: 0 8px 25px rgba(0, 242, 254, 0.4) !important;
        transform: translateY(-2px) !important;
    }}

    /* Custom Explore ERP Button */
    .explore-btn-container div.stButton > button {{
        min-height: 70px !important;
        padding: 18px 36px !important;
        border: 2px solid #00F2FE !important;
        background: linear-gradient(90deg, rgba(0, 242, 254, 0.25) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        box-shadow: 0 8px 25px rgba(0, 242, 254, 0.3) !important;
    }}

    .explore-btn-container div.stButton > button p,
    .explore-btn-container div.stButton > button span {{
        font-size: 22px !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
    }}

    /* KPI Cards Styling */
    .kpi-card-horizontal {{
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 12px;
        padding: 14px 16px;
        min-height: 85px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }}

    .kpi-card-horizontal:hover {{
        transform: translateY(-4px);
        border-color: #00F2FE;
        box-shadow: 0 8px 20px rgba(0, 242, 254, 0.3);
    }}

    .kpi-icon-box {{
        width: 42px;
        height: 42px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}

    .kpi-icon-box svg {{
        width: 22px;
        height: 22px;
    }}

    .kpi-details {{
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .kpi-title {{
        color: #CBD5E1 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .kpi-value {{
        font-size: 20px !important;
        font-weight: 800 !important;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background: rgba(10, 16, 30, 0.94) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 1px solid rgba(0, 242, 254, 0.25) !important;
    }}

    .sidebar-header-box {{
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        background: linear-gradient(90deg, rgba(0, 242, 254, 0.15) 0%, rgba(15, 23, 42, 0) 100%);
        border-left: 3px solid #00F2FE;
        border-radius: 4px;
        margin-bottom: 15px;
        margin-top: 10px;
    }}

    .sidebar-header-text {{
        font-size: 13px !important;
        font-weight: 800 !important;
        color: #00F2FE !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}

    [data-testid="stDataFrame"] {{
        background-color: rgba(15, 23, 42, 0.75) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        padding: 10px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# Fetch Database Data Safely 
@st.cache_data(ttl=300)
def load_data():
    conn = None
    try:
        conn = get_db_connection()
        df = pd.read_sql("SELECT * FROM Projects", conn)
        return df
    finally:
        if conn and conn.is_connected():
            conn.close()


try:
    projects = load_data()
except Exception as e:
    st.error(f"Database Connection Error: {e}")
    st.stop()


# Dynamic Header Logic according to active page
header_title = (
    "Solar Energy ERP Analytics Dashboard"
    if not st.session_state.view_dashboard
    else st.session_state.current_page
)

# Header Section 
st.markdown(
    f"""
    <div class="dashboard-title-container">
        <div class="title-icon-box">
            <svg fill="#00F2FE" width="28" height="28" viewBox="0 0 24 24">
                <path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zm0 8c-1.65 0-3-1.35-3-3s1.35-3 3-3 3 1.35 3 3-1.35 3-3 3zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0s-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0s-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06c.38-.38.38-1.02 0-1.41zM7.05 18.36l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06c.39-.39.39-1.03 0-1.41s-1.02-.39-1.41 0z"/>
            </svg>
        </div>
        <h1 class="main-title-text">{header_title}</h1>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PAGE 0: LANDING / HOME PAGE
# =========================================================
if not st.session_state.view_dashboard:
    st.subheader("Quick System Summary")

    total_all_projects = len(projects)
    total_val = (
        projects["Contract_Value"].sum() if "Contract_Value" in projects.columns else 0
    )
    total_cities = projects["City"].nunique() if "City" in projects.columns else 0

    sum1, sum2, sum3 = st.columns(3)
    with sum1:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-title">
                    <span class="material-symbols-outlined" style="color:#00F2FE;">assignment</span> Registered Projects
                </div>
                <div style="font-size: 22px; font-weight: 800; color: #FFFFFF; margin-top: 5px;">
                    {total_all_projects}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with sum2:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-title">
                    <span class="material-symbols-outlined" style="color:#00F2FE;">account_balance_wallet</span> Portfolio Value
                </div>
                <div style="font-size: 22px; font-weight: 800; color: #FFFFFF; margin-top: 5px;">
                    ₹{total_val:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with sum3:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-title">
                    <span class="material-symbols-outlined" style="color:#00F2FE;">location_city</span> Operational Cities
                </div>
                <div style="font-size: 22px; font-weight: 800; color: #FFFFFF; margin-top: 5px;">
                    {total_cities}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Key Operational Domains")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">
                    <span class="material-symbols-outlined" style="color:#00F2FE;">payments</span> Financial Metrics & Budgeting
                </div>
                <div style="font-size: 13px; color: #CBD5E1; margin-top: 5px;">
                    Track total contract values, estimated cost vs actual cost deviations, and key financial KPIs in a single window.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">
                    <span class="material-symbols-outlined" style="color:#00F2FE;">solar_power</span> Solar Installation Lifecycle
                </div>
                <div style="font-size: 13px; color: #CBD5E1; margin-top: 5px;">
                    Monitor status-wise distribution of ongoing, completed, delayed, and cancelled projects along with city/type breakdowns.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">
                    <span class="material-symbols-outlined" style="color:#00F2FE;">local_shipping</span> Hardware Supply Chain
                </div>
                <div style="font-size: 13px; color: #CBD5E1; margin-top: 5px;">
                    Analyze top suppliers by procurement value, material allocation status, and granular project-level record tables.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Explore ERP Dashboard Button
    st.markdown('<div class="explore-btn-container">', unsafe_allow_html=True)
    if st.button(
        "EXPLORE ERP DASHBOARD",
        use_container_width=True,
    ):
        go_to_dashboard()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# DASHBOARD PAGES
# =========================================================
else:
    # --- Sidebar Title Section ---
    st.sidebar.markdown(
        """
        <div style="
            text-align: center;
            padding: 16px 12px;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(0, 242, 254, 0.08) 100%);
            border: 1px solid rgba(0, 242, 254, 0.4);
            border-radius: 14px;
            margin-bottom: 18px;
            box-shadow: 0 8px 25px rgba(0, 242, 254, 0.15);
            backdrop-filter: blur(10px);
        ">
            <div style="
                font-size: 16px;
                font-weight: 800;
                background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 50%, #FFFFFF 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: 0.8px;
                line-height: 1.4;
                filter: drop-shadow(0px 0px 8px rgba(0, 242, 254, 0.6));
                text-transform: uppercase;
            ">
                Solar Energy ERP<br>Analytics Dashboard
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar Back to Overview Button 
    if st.sidebar.button("← Back to Overview", use_container_width=True):
        go_to_home()
        st.rerun()

    st.sidebar.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

    # Sidebar Header
    st.sidebar.markdown(
        """
        <div class="sidebar-header-box">
            <span class="sidebar-header-text">NAVIGATION MENU</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_items = [
        ("Operational Metrics", "Operational Metrics", ":material/dashboard:"),
        (
            "Project Progress Tracking",
            "Project Progress Tracking",
            ":material/trending_up:",
        ),
        (
            "Financial Performance",
            "Financial Performance",
            ":material/payments:",
        ),
        (
            "Procurement & Inventory",
            "Procurement & Inventory",
            ":material/inventory_2:",
        ),
    ]

    for label, target_page, icon_name in nav_items:
        is_active = st.session_state.current_page == target_page
        display_label = f"✓ {label}" if is_active else label

        if st.sidebar.button(
            display_label,
            key=f"nav_{target_page}",
            icon=icon_name,
            use_container_width=True,
        ):
            st.session_state.current_page = target_page
            st.rerun()

    page = st.session_state.current_page

    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    # Sidebar Filter Options
    st.sidebar.markdown(
        """
        <div class="sidebar-header-box">
            <span class="sidebar-header-text">FILTER OPTIONS</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    status_options = (
        ["All"] + sorted(projects["Project_Status"].dropna().unique().tolist())
        if "Project_Status" in projects.columns
        else ["All"]
    )
    selected_status = st.sidebar.selectbox("Project Status", status_options)

    type_options = (
        ["All"] + sorted(projects["Project_Type"].dropna().unique().tolist())
        if "Project_Type" in projects.columns
        else ["All"]
    )
    selected_type = st.sidebar.selectbox("Project Type", type_options)

    customer_options = (
        ["All"]
        + sorted(
            projects["Customer_ID"].dropna().astype(str).unique().tolist()
        )
        if "Customer_ID" in projects.columns
        else ["All"]
    )
    selected_customer = st.sidebar.selectbox("Customer", customer_options)

    city_options = (
        ["All"] + sorted(projects["City"].dropna().unique().tolist())
        if "City" in projects.columns
        else ["All"]
    )
    selected_city = st.sidebar.selectbox("City", city_options)

    min_cost = (
        float(projects["Estimated_Cost"].min())
        if "Estimated_Cost" in projects.columns
        else 0.0
    )
    max_cost = (
        float(projects["Estimated_Cost"].max())
        if "Estimated_Cost" in projects.columns
        else 1000000.0
    )
    selected_cost = st.sidebar.slider(
        "Estimated Cost Range",
        min_value=min_cost,
        max_value=max_cost,
        value=(min_cost, max_cost),
    )

    # Filtering Logic
    filtered_projects = projects.copy()

    if selected_status != "All" and "Project_Status" in filtered_projects.columns:
        filtered_projects = filtered_projects[
            filtered_projects["Project_Status"] == selected_status
        ]

    if selected_type != "All" and "Project_Type" in filtered_projects.columns:
        filtered_projects = filtered_projects[
            filtered_projects["Project_Type"] == selected_type
        ]

    if selected_customer != "All" and "Customer_ID" in filtered_projects.columns:
        filtered_projects = filtered_projects[
            filtered_projects["Customer_ID"].astype(str) == selected_customer
        ]

    if selected_city != "All" and "City" in filtered_projects.columns:
        filtered_projects = filtered_projects[
            filtered_projects["City"] == selected_city
        ]

    if "Estimated_Cost" in filtered_projects.columns:
        filtered_projects = filtered_projects[
            (filtered_projects["Estimated_Cost"] >= selected_cost[0])
            & (filtered_projects["Estimated_Cost"] <= selected_cost[1])
        ]

    total_projects = len(filtered_projects)
    completed_projects = (
        (filtered_projects["Project_Status"] == "Completed").sum()
        if "Project_Status" in filtered_projects.columns
        else 0
    )
    ongoing_projects = (
        (filtered_projects["Project_Status"] == "Ongoing").sum()
        if "Project_Status" in filtered_projects.columns
        else 0
    )
    delayed_projects = (
        (filtered_projects["Project_Status"] == "Delayed").sum()
        if "Project_Status" in filtered_projects.columns
        else 0
    )
    cancelled_projects = (
        (filtered_projects["Project_Status"] == "Cancelled").sum()
        if "Project_Status" in filtered_projects.columns
        else 0
    )

    total_estimated_cost = (
        filtered_projects["Estimated_Cost"].sum()
        if "Estimated_Cost" in filtered_projects.columns
        else 0
    )
    total_actual_cost = (
        filtered_projects["Actual_Cost"].sum()
        if "Actual_Cost" in filtered_projects.columns
        else 0
    )
    total_contract_value = (
        filtered_projects["Contract_Value"].sum()
        if "Contract_Value" in filtered_projects.columns
        else 0
    )

    # Page 1: Operational Metrics 
    if page == "Operational Metrics":
        st.subheader("Project Overview")

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(
                f"""<div class="kpi-card-horizontal"><div class="kpi-icon-box" style="background: rgba(0, 242, 254, 0.2);"><svg fill="#00F2FE" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg></div><div class="kpi-details"><div class="kpi-title">Total Projects</div><div class="kpi-value" style="color: #00F2FE !important;">{total_projects}</div></div></div>""",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""<div class="kpi-card-horizontal"><div class="kpi-icon-box" style="background: rgba(16, 185, 129, 0.2);"><svg fill="#10B981" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg></div><div class="kpi-details"><div class="kpi-title">Completed</div><div class="kpi-value" style="color: #10B981 !important;">{completed_projects}</div></div></div>""",
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f"""<div class="kpi-card-horizontal"><div class="kpi-icon-box" style="background: rgba(245, 158, 11, 0.2);"><svg fill="#F59E0B" viewBox="0 0 24 24"><path d="M11 15h2v2h-2zm0-8h2v6h-2zm1-5C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/></svg></div><div class="kpi-details"><div class="kpi-title">Ongoing</div><div class="kpi-value" style="color: #F59E0B !important;">{ongoing_projects}</div></div></div>""",
                unsafe_allow_html=True,
            )
        with col4:
            st.markdown(
                f"""<div class="kpi-card-horizontal"><div class="kpi-icon-box" style="background: rgba(249, 115, 22, 0.2);"><svg fill="#F97316" viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/></svg></div><div class="kpi-details"><div class="kpi-title">Delayed</div><div class="kpi-value" style="color: #F97316 !important;">{delayed_projects}</div></div></div>""",
                unsafe_allow_html=True,
            )
        with col5:
            st.markdown(
                f"""<div class="kpi-card-horizontal"><div class="kpi-icon-box" style="background: rgba(239, 68, 68, 0.2);"><svg fill="#EF4444" viewBox="0 0 24 24"><path d="M12 2C6.47 2 2 6.48 2 12s4.47 10 10 10 10-4.48 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"/></svg></div><div class="kpi-details"><div class="kpi-title">Cancelled</div><div class="kpi-value" style="color: #EF4444 !important;">{cancelled_projects}</div></div></div>""",
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Financial Overview Summary")
        fin1, fin2, fin3 = st.columns(3)

        with fin1:
            st.markdown(
                f"""<div class="kpi-card-horizontal"><div class="kpi-icon-box" style="background: rgba(0, 242, 254, 0.2);"><svg fill="#00F2FE" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg></div><div class="kpi-details"><div class="kpi-title">Total Contract Value</div><div class="kpi-value" style="color: #00F2FE !important;">₹{total_contract_value:,.0f}</div></div></div>""",
                unsafe_allow_html=True,
            )
        with fin2:
            st.markdown(
                f"""<div class="kpi-card-horizontal"><div class="kpi-icon-box" style="background: rgba(59, 130, 246, 0.2);"><svg fill="#3B82F6" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg></div><div class="kpi-details"><div class="kpi-title">Estimated Cost</div><div class="kpi-value" style="color: #3B82F6 !important;">₹{total_estimated_cost:,.0f}</div></div></div>""",
                unsafe_allow_html=True,
            )
        with fin3:
            st.markdown(
                f"""<div class="kpi-card-horizontal"><div class="kpi-icon-box" style="background: rgba(6, 182, 212, 0.2);"><svg fill="#06B6D4" viewBox="0 0 24 24"><path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1H7c.12 2.19 1.76 3.42 3.8 3.84V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/></svg></div><div class="kpi-details"><div class="kpi-title">Actual Cost</div><div class="kpi-value" style="color: #06B6D4 !important;">₹{total_actual_cost:,.0f}</div></div></div>""",
                unsafe_allow_html=True,
            )

    # Page 2: Project Progress Tracking 
    elif page == "Project Progress Tracking":
        st.subheader("1. Project Status Distribution")
        if (
            not filtered_projects.empty
            and "Project_Status" in filtered_projects.columns
        ):
            status_count = (
                filtered_projects["Project_Status"].value_counts().reset_index()
            )
            status_count.columns = ["Project_Status", "Count"]

            fig1 = px.bar(
                status_count,
                x="Project_Status",
                y="Count",
                text="Count",
                color="Project_Status",
                color_discrete_map={
                    "Completed": "#00F2FE",
                    "Ongoing": "#3B82F6",
                    "Delayed": "#6366F1",
                    "Cancelled": "#64748B",
                },
            )
            fig1.update_traces(textposition="outside")
            fig1.update_layout(
                xaxis_title="Status", yaxis_title="Number of Projects"
            )
            apply_white_theme(fig1)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No project status data available.")

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.subheader("2. Projects Share by Category/Type")
        if (
            not filtered_projects.empty
            and "Project_Type" in filtered_projects.columns
        ):
            project_type_count = (
                filtered_projects["Project_Type"].value_counts().reset_index()
            )
            project_type_count.columns = ["Project_Type", "Total_Projects"]

            fig2 = px.pie(
                project_type_count,
                names="Project_Type",
                values="Total_Projects",
                hole=0.45,
            )
            fig2.update_traces(
                marker=dict(
                    colors=[
                        "#00F2FE",
                        "#00C6FF",
                        "#0072FF",
                        "#3A7BD5",
                        "#22E135",
                    ]
                ),
                textinfo="percent+label",
            )
            apply_white_theme(fig2)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No project type data available.")

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.subheader("3. Top 10 Cities by Active Projects")
        if not filtered_projects.empty and "City" in filtered_projects.columns:
            city_counts = (
                filtered_projects["City"].value_counts().head(10).reset_index()
            )
            city_counts.columns = ["City", "Project_Count"]

            fig_city = px.bar(
                city_counts,
                x="City",
                y="Project_Count",
                text="Project_Count",
                color="Project_Count",
                color_continuous_scale="Blues",
            )
            fig_city.update_traces(textposition="outside")
            fig_city.update_layout(xaxis_title="City", yaxis_title="Projects")
            apply_white_theme(fig_city)
            st.plotly_chart(fig_city, use_container_width=True)
        else:
            st.info("No city data available.")

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.subheader("4. Project Completion Status Breakdown by Type")
        if (
            not filtered_projects.empty
            and "Project_Type" in filtered_projects.columns
            and "Project_Status" in filtered_projects.columns
        ):
            type_status = (
                filtered_projects.groupby(["Project_Type", "Project_Status"])
                .size()
                .reset_index(name="Count")
            )
            fig_type_status = px.bar(
                type_status,
                x="Project_Type",
                y="Count",
                color="Project_Status",
                barmode="group",
                color_discrete_map={
                    "Completed": "#00F2FE",
                    "Ongoing": "#3B82F6",
                    "Delayed": "#FF6B00",
                    "Cancelled": "#991B1B",
                },
            )
            fig_type_status.update_layout(
                xaxis_title="Project Type", yaxis_title="Count"
            )
            apply_white_theme(fig_type_status)
            st.plotly_chart(fig_type_status, use_container_width=True)
        else:
            st.info("Insufficient breakdown data.")

    # Page 3: Financial Performance 
    elif page == "Financial Performance":
        st.subheader("1. Total Estimated Cost vs Actual Cost Comparison")
        cost_data = pd.DataFrame(
            {
                "Cost Type": ["Estimated Cost", "Actual Cost"],
                "Amount": [total_estimated_cost, total_actual_cost],
            }
        )

        fig5 = px.bar(
            cost_data,
            x="Cost Type",
            y="Amount",
            text="Amount",
            color="Cost Type",
            color_discrete_map={
                "Estimated Cost": "#3B82F6",
                "Actual Cost": "#06B6D4",
            },
        )
        fig5.update_traces(
            texttemplate="₹%{text:,.0f}", textposition="outside"
        )
        fig5.update_layout(xaxis_title="Cost Type", yaxis_title="Amount (₹)")
        apply_white_theme(fig5)
        st.plotly_chart(fig5, use_container_width=True)

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.subheader("2. Monthly Contract Value Trend")
        if (
            not filtered_projects.empty
            and "Expected_Completion" in filtered_projects.columns
        ):
            monthly_data = filtered_projects.copy()
            monthly_data["Expected_Completion"] = pd.to_datetime(
                monthly_data["Expected_Completion"], errors="coerce"
            )
            monthly_data = monthly_data.dropna(
                subset=["Expected_Completion", "Contract_Value"]
            )

            if not monthly_data.empty:
                monthly_contract = (
                    monthly_data.groupby(
                        monthly_data["Expected_Completion"].dt.to_period("M")
                    )["Contract_Value"]
                    .sum()
                    .reset_index()
                )
                monthly_contract["Month"] = monthly_contract[
                    "Expected_Completion"
                ].dt.strftime("%b %Y")

                fig3 = px.line(
                    monthly_contract,
                    x="Month",
                    y="Contract_Value",
                    markers=True,
                    text="Contract_Value",
                )
                fig3.update_traces(
                    line=dict(color="#00F2FE", width=3.5),
                    texttemplate="₹%{text:,.0f}",
                )
                fig3.update_layout(
                    xaxis_title="Month", yaxis_title="Contract Value (₹)"
                )
                apply_white_theme(fig3)
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No valid monthly timeline data available.")
        else:
            st.info("Timeline column missing.")

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.subheader("3. Cost Variance (Actual - Estimated) by City")
        if not filtered_projects.empty and "City" in filtered_projects.columns:
            city_cost = (
                filtered_projects.groupby("City")[
                    ["Estimated_Cost", "Actual_Cost"]
                ]
                .sum()
                .reset_index()
            )
            city_cost["Variance"] = (
                city_cost["Actual_Cost"] - city_cost["Estimated_Cost"]
            )
            city_cost = city_cost.sort_values(
                by="Variance", ascending=False
            ).head(10)

            fig_var = px.bar(
                city_cost,
                x="Variance",
                y="City",
                orientation="h",
                color="Variance",
                color_continuous_scale="Blues",
                text="Variance",
            )
            fig_var.update_traces(
                texttemplate="₹%{text:,.0f}", textposition="outside"
            )
            fig_var.update_layout(
                xaxis_title="Cost Difference (Overrun / Savings)",
                yaxis_title="City",
            )
            apply_white_theme(fig_var)
            st.plotly_chart(fig_var, use_container_width=True)
        else:
            st.info("No cost variance data by city.")

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.subheader("4. Contract Value Distribution by Project Type")
        if (
            not filtered_projects.empty
            and "Project_Type" in filtered_projects.columns
            and "Contract_Value" in filtered_projects.columns
        ):
            fig_violin = px.violin(
                filtered_projects,
                x="Project_Type",
                y="Contract_Value",
                color="Project_Type",
                box=True,
                points="all",
                color_discrete_sequence=[
                    "#00F2FE",
                    "#3B82F6",
                    "#00C6FF",
                    "#4FACFE",
                    "#2563EB",
                ],
            )
            fig_violin.update_layout(
                xaxis_title="Project Type", yaxis_title="Contract Value (₹)"
            )
            apply_white_theme(fig_violin)
            st.plotly_chart(fig_violin, use_container_width=True)
        else:
            st.info("Distribution data unavailable.")

    # Page 4: Procurement & Details 
    elif page == "Procurement & Inventory":
        st.subheader("1. Top 10 Suppliers by Procurement Amount")
        conn = None
        try:
            conn = get_db_connection()
            supplier_query = """
                SELECT pr.Supplier_ID, SUM(pr.Total_Amount) AS Total_Procurement
                FROM Procurement pr
                INNER JOIN Projects p ON pr.Project_ID = p.Project_ID
                GROUP BY pr.Supplier_ID
                ORDER BY Total_Procurement DESC
                LIMIT 10
            """
            procurement = pd.read_sql(supplier_query, conn)

            if not procurement.empty:
                fig4 = px.bar(
                    procurement,
                    x="Total_Procurement",
                    y="Supplier_ID",
                    orientation="h",
                    color="Total_Procurement",
                    color_continuous_scale="Blues",
                    text="Total_Procurement",
                )
                fig4.update_traces(
                    texttemplate="₹%{text:,.0f}", textposition="outside"
                )
                fig4.update_layout(
                    xaxis_title="Total Amount (₹)",
                    yaxis_title="Supplier ID",
                    coloraxis_showscale=False,
                )
                apply_white_theme(fig4)
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("No procurement records found.")
        except Exception as err:
            st.info(f"Procurement DB query failed or table unavailable: {err}")
        finally:
            if conn and conn.is_connected():
                conn.close()

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.subheader("2. Top 10 Projects by Procurement Spend")
        conn_proj = None
        try:
            conn_proj = get_db_connection()
            proj_proc_query = """
                SELECT pr.Project_ID, SUM(pr.Total_Amount) AS Project_Procurement
                FROM Procurement pr
                GROUP BY pr.Project_ID
                ORDER BY Project_Procurement DESC
                LIMIT 10
            """
            proj_proc = pd.read_sql(proj_proc_query, conn_proj)

            if not proj_proc.empty:
                fig_p_proc = px.bar(
                    proj_proc,
                    x="Project_Procurement",
                    y="Project_ID",
                    orientation="h",
                    color="Project_Procurement",
                    color_continuous_scale="Tealgrn",
                    text="Project_Procurement",
                )
                fig_p_proc.update_traces(
                    texttemplate="₹%{text:,.0f}", textposition="outside"
                )
                fig_p_proc.update_layout(
                    xaxis_title="Procurement Cost (₹)",
                    yaxis_title="Project ID",
                    coloraxis_showscale=False,
                )
                apply_white_theme(fig_p_proc)
                st.plotly_chart(fig_p_proc, use_container_width=True)
            else:
                st.info("No project procurement data found.")
        except Exception:
            st.info("Project-wise procurement data unavailable.")
        finally:
            if conn_proj and conn_proj.is_connected():
                conn_proj.close()

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.subheader("3. Estimated vs Actual Cost Comparison by Status")
        if (
            not filtered_projects.empty
            and "Project_Status" in filtered_projects.columns
        ):
            status_costs = (
                filtered_projects.groupby("Project_Status")[
                    ["Estimated_Cost", "Actual_Cost"]
                ]
                .mean()
                .reset_index()
            )
            fig_status_costs = px.bar(
                status_costs,
                x="Project_Status",
                y=["Estimated_Cost", "Actual_Cost"],
                barmode="group",
                color_discrete_sequence=["#3B82F6", "#06B6D4"],
            )
            fig_status_costs.update_layout(
                xaxis_title="Project Status", yaxis_title="Average Cost (₹)"
            )
            apply_white_theme(fig_status_costs)
            st.plotly_chart(fig_status_costs, use_container_width=True)
        else:
            st.info("Cost comparison by status unavailable.")

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.subheader("4. Project Detailed Data View")
        display_columns = [
            col
            for col in [
                "Project_ID",
                "Project_Type",
                "Project_Status",
                "City",
                "Contract_Value",
                "Estimated_Cost",
                "Actual_Cost",
            ]
            if col in filtered_projects.columns
        ]
        st.dataframe(
            filtered_projects[display_columns],
            use_container_width=True,
            hide_index=True,
        )