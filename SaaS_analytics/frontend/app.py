# app.py
"""
SaaS Business Analytics & Prediction Platform
Main Router and Streamlit Entrypoint.
Handles session states, global styling injection, multipage sidebar routing,
datasets loading, and the global secure SMTP configurations form.
"""

import time
import os
import sys

# Dynamic path resolution: Add project root, frontend, and backend folders to search paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) if os.path.basename(current_dir) == "frontend" else current_dir

for path in [project_root, os.path.join(project_root, "frontend"), os.path.join(project_root, "backend")]:
    if path not in sys.path:
        sys.path.append(path)

import streamlit as st
import smtplib
from utils.data_loader import load_saas_sales_data, load_churn_data, process_custom_sales_data, process_custom_churn_data
from utils.email_service import MOCK_EMAIL_LOG, send_logout_email_async
from components.login import render_login_page
from components.sales_dashboard import render_sales_dashboard
from components.retention_cohort import render_retention_cohort
from components.churn_predictor import render_churn_predictor

# 1. Global Streamlit Layout Page Settings
st.set_page_config(
    page_title="SaaS Revenue & Churn Analytics Portal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Session State Initialization
def load_env_config():
    env_vars = {}
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir) if os.path.basename(current_dir) == "frontend" else current_dir
    env_path = os.path.join(project_root, "backend", ".env")
    if not os.path.exists(env_path):
        env_path = os.path.join(project_root, ".env")
        
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    env_vars[key.strip()] = val.strip()
    return env_vars

env_config = load_env_config()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "smtp_settings" not in st.session_state:
    if "smtp" in st.secrets:
        host = st.secrets["smtp"].get("host", "smtp.gmail.com")
        username = st.secrets["smtp"].get("username", "")
        if "gmail.com" in username.lower() and "sendgrid" in host.lower():
            host = "smtp.gmail.com"
        st.session_state.smtp_settings = {
            "demo_mode": st.secrets["smtp"].get("demo_mode", False),
            "host": host,
            "port": int(st.secrets["smtp"].get("port", 587)),
            "username": username,
            "password": st.secrets["smtp"].get("password", ""),
            "sender_email": st.secrets["smtp"].get("sender_email", st.secrets["smtp"].get("from_email", ""))
        }
    else:
        host = env_config.get("SMTP_HOST", "smtp.gmail.com")
        username = env_config.get("SMTP_USERNAME", "")
        if "gmail.com" in username.lower() and "sendgrid" in host.lower():
            host = "smtp.gmail.com"
        has_env = "SMTP_HOST" in env_config
        st.session_state.smtp_settings = {
            "demo_mode": not has_env,
            "host": host,
            "port": int(env_config.get("SMTP_PORT", 587)),
            "username": username,
            "password": env_config.get("SMTP_PASSWORD", ""),
            "sender_email": env_config.get("EMAIL_FROM", "")
        }

# 3. Handle Login Page Routing
if not st.session_state.logged_in:
    # Render Login Portal (Email/Password & Google Federated authentication)
    render_login_page()
    
    # Sub-footer spacer on Login Screen
    st.markdown('<div class="login-container" style="margin-top: -20px;"></div>', unsafe_allow_html=True)

# 4. Handle Logged-In Application Layout
else:
    # Load CSS globally
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(current_dir, "styles.css") if os.path.basename(current_dir) == "frontend" else os.path.join(current_dir, "frontend", "styles.css")
        if not os.path.exists(css_path):
            css_path = os.path.join(current_dir, "styles.css")
            
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Styling load error: {e}")
        
    # Lazy load both datasets
    try:
        df_sales = load_saas_sales_data()
        df_churn = load_churn_data()
    except Exception as e:
        st.error(f"Critical error loading core platform datasets: {e}")
        st.stop()
        
    # --- PREMIUM SIDEBAR ROUTING ---
    with st.sidebar:
        # Platform Branding Logo
        st.markdown(
            """
            <div style="padding: 10px 0; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 20px;">
                <span class="platform-title" style="font-size: 1.4rem; background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 50%, #00cec9 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Executive Analytics</span>
                <p style="color: #636e72; font-size: 0.75rem; margin-top: 5px; text-transform: uppercase; letter-spacing: 0.5px;">SaaS Revenue & Churn BI</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # User details profile card
        st.markdown(
            f"""
            <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; margin-bottom: 20px;">
                <div style="font-size: 0.75rem; color: #a0a0c0; text-transform: uppercase; letter-spacing: 0.5px;">Logged in as:</div>
                <div style="font-size: 0.88rem; font-weight: 600; color: #ffffff; margin-top: 3px; word-break: break-all;">{st.session_state.user_email}</div>
                <div style="display: inline-block; font-size: 0.65rem; color: #00cec9; background: rgba(0, 206, 201, 0.1); padding: 2px 6px; border-radius: 4px; margin-top: 5px; font-weight: bold;">
                    Active Session
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Navigation Menu
        st.markdown('<div class="metric-label" style="font-size: 0.75rem; margin-bottom: 5px;">Platform Workspaces</div>', unsafe_allow_html=True)
        workspace = st.radio(
            "Select Workspace",
            [
                "📊 Executive Sales Dashboard", 
                "📈 Retention Cohort Matrix", 
                "🔮 Churn Predictor"
            ],
            label_visibility="collapsed"
        )
        
        # Dataset Source Selector Panel
        st.markdown('<div class="metric-label" style="font-size: 0.75rem; margin-top: 20px; margin-bottom: 5px;">💾 DATASET SOURCE</div>', unsafe_allow_html=True)
        dataset_source = st.radio(
            "Dataset Source Selection",
            ["System Default Datasets", "Upload Custom CSV 📂"],
            label_visibility="collapsed"
        )
        
        # Initialize custom dataset states
        if "custom_sales_df" not in st.session_state:
            st.session_state.custom_sales_df = None
        if "custom_sales_absent" not in st.session_state:
            st.session_state.custom_sales_absent = []
        if "custom_churn_df" not in st.session_state:
            st.session_state.custom_churn_df = None
        if "custom_churn_absent" not in st.session_state:
            st.session_state.custom_churn_absent = []
            
        if dataset_source == "Upload Custom CSV 📂":
            st.markdown('<div style="margin-top: 5px;"></div>', unsafe_allow_html=True)
            if "Executive Sales" in workspace or "Retention Cohort" in workspace:
                uploaded_sales = st.file_uploader(
                    "Upload Sales CSV",
                    type=["csv"],
                    help="Transaction CSV with Sales, Profit, Quantity, Order Date, Customer ID."
                )
                if uploaded_sales is not None:
                    try:
                        if "last_sales_filename" not in st.session_state or st.session_state.last_sales_filename != uploaded_sales.name:
                            df_custom, absent = process_custom_sales_data(uploaded_sales)
                            st.session_state.custom_sales_df = df_custom
                            st.session_state.custom_sales_absent = absent
                            st.session_state.last_sales_filename = uploaded_sales.name
                            st.success("Custom sales dataset loaded successfully!")
                            time.sleep(0.5)
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error parsing sales CSV: {e}")
            elif "Churn Predictor" in workspace:
                uploaded_churn = st.file_uploader(
                    "Upload Churn CSV",
                    type=["csv"],
                    help="Customer Churn CSV with characteristics and 'Churn' target."
                )
                if uploaded_churn is not None:
                    try:
                        if "last_churn_filename" not in st.session_state or st.session_state.last_churn_filename != uploaded_churn.name:
                            df_custom, absent = process_custom_churn_data(uploaded_churn)
                            st.session_state.custom_churn_df = df_custom
                            st.session_state.custom_churn_absent = absent
                            st.session_state.last_churn_filename = uploaded_churn.name
                            st.cache_resource.clear()
                            st.success("Custom churn dataset loaded successfully!")
                            time.sleep(0.5)
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error parsing churn CSV: {e}")
        
        st.markdown('<div style="margin-top: 30px;"></div>', unsafe_allow_html=True)
        
        # Logout action
        if st.button("Sign Out Session", key="btn_logout"):
            # Trigger Asynchronous SMTP Logout Email Notification
            smtp_conf = st.session_state.get("smtp_settings", {"demo_mode": True})
            send_logout_email_async(st.session_state.user_email, smtp_config=smtp_conf)
            time.sleep(0.5)
            
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.rerun()

    # Resolve active datasets & absent elements list
    active_sales_df    = df_sales
    active_sales_absent = []
    active_churn_df    = df_churn
    active_churn_absent = []

    try:
        if dataset_source == "Upload Custom CSV 📂":
            if st.session_state.custom_sales_df is not None and (
                "Executive Sales" in workspace or "Retention Cohort" in workspace
            ):
                active_sales_df     = st.session_state.custom_sales_df
                active_sales_absent = st.session_state.get("custom_sales_absent", [])
            if st.session_state.custom_churn_df is not None and "Churn Predictor" in workspace:
                active_churn_df     = st.session_state.custom_churn_df
                active_churn_absent = st.session_state.get("custom_churn_absent", [])
    except Exception as e:
        st.warning(f"Dataset resolution issue: {e}")

    # Inject absent lists globally so components can access them
    st.session_state.active_sales_absent = active_sales_absent
    st.session_state.active_churn_absent = active_churn_absent

    # --- ROUTE TO ACTIVE WORKSPACE PANEL ---
    if "Executive Sales" in workspace:
        if dataset_source == "Upload Custom CSV 📂" and st.session_state.custom_sales_df is None:
            st.markdown('<h1 class="platform-title" style="text-align: left; font-size: 2.2rem; margin-bottom: 5px;">Executive Sales Analytics Workspace</h1>', unsafe_allow_html=True)
            st.info("📂 Please upload your SaaS Sales Transaction CSV in the sidebar panel to view your results!")
        else:
            try:
                render_sales_dashboard(active_sales_df)
            except Exception as e:
                st.error(f"⚠️ Sales Dashboard encountered an error: {e}")

    elif "Retention Cohort" in workspace:
        if dataset_source == "Upload Custom CSV 📂" and st.session_state.custom_sales_df is None:
            st.markdown('<h1 class="platform-title" style="text-align: left; font-size: 2.2rem; margin-bottom: 5px;">Retention Cohort Matrix</h1>', unsafe_allow_html=True)
            st.info("📂 Please upload your SaaS Sales Transaction CSV in the sidebar panel to view your results!")
        else:
            try:
                render_retention_cohort(active_sales_df)
            except Exception as e:
                st.error(f"⚠️ Retention Cohort encountered an error: {e}")

    elif "Churn Predictor" in workspace:
        if dataset_source == "Upload Custom CSV 📂" and st.session_state.custom_churn_df is None:
            st.markdown('<h1 class="platform-title" style="text-align: left; font-size: 2.2rem; margin-bottom: 5px;">Customer Churn Risk Analysis</h1>', unsafe_allow_html=True)
            st.info("📂 Please upload your Customer Churn CSV in the sidebar panel to run model predictions!")
        else:
            try:
                render_churn_predictor(active_churn_df)
            except Exception as e:
                st.error(f"⚠️ Churn Predictor encountered an error: {e}")

    pass
