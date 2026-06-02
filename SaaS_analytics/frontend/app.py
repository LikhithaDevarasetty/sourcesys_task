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
from utils.data_loader import load_saas_sales_data, load_churn_data
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

def handle_google_oauth_callback():
    code = st.query_params.get("code")
    state = st.query_params.get("state")
    
    if code:
        st.query_params.clear()
        
        from components.login import get_google_oauth_secrets
        creds = get_google_oauth_secrets()
        client_id = creds.get("client_id")
        client_secret = creds.get("client_secret")
        redirect_uri = creds.get("redirect_uri", "https://likhithadevarasetty-sourcesys--saas-analyticsfrontendapp-cqtwwz.streamlit.app/component/streamlit_oauth.authorize_button/")
        
        if not client_id or not client_secret:
            st.error("Google OAuth secrets are not fully configured. Cannot complete sign-in.")
            return
            
        import requests
        import base64
        import json
        import urllib.parse
        
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        
        try:
            res = requests.post(token_url, data=data, timeout=10)
            if res.status_code != 200:
                st.error(f"Failed to authenticate with Google: {res.text}")
                return
                
            token_info = res.json()
            id_token = token_info.get("id_token")
            
            if not id_token:
                st.error("No ID token returned by Google.")
                return
                
            parts = id_token.split(".")
            if len(parts) < 2:
                st.error("Malformed JWT ID token returned by Google.")
                return
                
            payload_b64 = parts[1]
            payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
            payload_json = base64.urlsafe_b64decode(payload_b64).decode("utf-8")
            user_info = json.loads(payload_json)
            
            email = user_info.get("email")
            name = user_info.get("name")
            
            if not email:
                st.error("Google account did not return a valid email address.")
                return
                
            email_clean = email.strip().lower()
            
            from utils.auth_db import load_users, register_user
            users = load_users()
            smtp_conf = st.session_state.get("smtp_settings", {"demo_mode": True})
            
            if state and state.startswith("signup:"):
                display_name = urllib.parse.unquote(state.split(":", 1)[1])
                
                if email_clean in users:
                    st.success("Welcome back! An account with this Google email already exists.")
                else:
                    success, msg = register_user(display_name, email_clean, "google_federated_pass_123")
                    if success:
                        send_welcome_email_async(email_clean, display_name, smtp_conf)
                    else:
                        st.error(f"Error provisioning your account: {msg}")
                        return
                
                st.session_state.logged_in = True
                st.session_state.user_email = email_clean
                st.rerun()
                
            else:
                if email_clean not in users:
                    st.error(f"No account found for '{email_clean}'. Please select 'Create an Account' first and sign up with Google!")
                    time.sleep(3.0)
                    return
                else:
                    client_details = {"ip": "127.0.0.1 (Google OAuth)", "browser": "Chrome / Windows OS"}
                    send_login_email_async(email_clean, smtp_conf, client_details)
                    
                    st.success(f"Welcome back, {users[email_clean]['name']}! Loading dashboard...")
                    time.sleep(0.8)
                    
                    st.session_state.logged_in = True
                    st.session_state.user_email = email_clean
                    st.rerun()
                    
        except Exception as e:
            st.error(f"Authentication exception occurred: {str(e)}")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "smtp_settings" not in st.session_state:
    if "smtp" in st.secrets:
        st.session_state.smtp_settings = {
            "demo_mode": st.secrets["smtp"].get("demo_mode", False),
            "host": st.secrets["smtp"].get("host", "smtp.gmail.com"),
            "port": int(st.secrets["smtp"].get("port", 587)),
            "username": st.secrets["smtp"].get("username", ""),
            "password": st.secrets["smtp"].get("password", ""),
            "sender_email": st.secrets["smtp"].get("sender_email", "")
        }
    else:
        has_env = "SMTP_HOST" in env_config
        st.session_state.smtp_settings = {
            "demo_mode": not has_env,
            "host": env_config.get("SMTP_HOST", "smtp.gmail.com"),
            "port": int(env_config.get("SMTP_PORT", 587)),
            "username": env_config.get("SMTP_USERNAME", ""),
            "password": env_config.get("SMTP_PASSWORD", ""),
            "sender_email": env_config.get("EMAIL_FROM", "")
        }

# Execute dynamic callback intercept before rendering page routing
handle_google_oauth_callback()


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
        st.markdown('<div class="metric-label" style="font-size: 0.75rem; margin-bottom: 10px;">Platform Workspaces</div>', unsafe_allow_html=True)
        workspace = st.radio(
            "Select Workspace",
            [
                "📊 Executive Sales Dashboard", 
                "📈 Retention Cohort Matrix", 
                "🔮 Churn Predictor"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)
        
        # Logout action
        if st.button("Sign Out Session", key="btn_logout"):
            # Trigger Asynchronous SMTP Logout Email Notification
            smtp_conf = st.session_state.get("smtp_settings", {"demo_mode": True})
            send_logout_email_async(st.session_state.user_email, smtp_config=smtp_conf)
            time.sleep(0.5)
            
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.rerun()

    # --- ROUTE TO ACTIVE WORKSPACE PANEL ---
    if "Executive Sales" in workspace:
        render_sales_dashboard(df_sales)
        
    elif "Retention Cohort" in workspace:
        render_retention_cohort(df_sales)
        
    elif "Churn Predictor" in workspace:
        render_churn_predictor(df_churn)
        
    pass
