# components/login.py
import time
import os
import streamlit as st
from utils.email_service import send_login_email_async, send_password_reset_email_async, send_welcome_email_async
from utils.auth_db import verify_user, register_user
import json

def get_google_oauth_secrets():
    # 1. Try Streamlit Secrets first
    if "google_oauth" in st.secrets:
        return {
            "client_id": st.secrets["google_oauth"].get("client_id"),
            "client_secret": st.secrets["google_oauth"].get("client_secret"),
            "redirect_uri": st.secrets["google_oauth"].get("redirect_uri", "http://localhost:8501")
        }
    
    # 2. Try local git-ignored JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir) if os.path.basename(current_dir) == "frontend" else current_dir
    creds_path = os.path.join(project_root, "backend", "google_creds.json")
    
    if os.path.exists(creds_path):
        try:
            with open(creds_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            pass
            
    return {}


def render_login_page():
    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "login"
    if "reset_token" not in st.session_state:
        st.session_state.reset_token = None
    if "reset_email" not in st.session_state:
        st.session_state.reset_email = None
        
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(current_dir, "..", "styles.css")
        if not os.path.exists(css_path):
            css_path = os.path.join(current_dir, "styles.css")
            
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        pass


    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    if st.session_state.auth_page == "login":
        _render_login_view()
    elif st.session_state.auth_page == "signup":
        _render_signup_view()
    elif st.session_state.auth_page == "forgot_password":
        _render_forgot_password_view()
    elif st.session_state.auth_page == "reset_password":
        _render_reset_password_view()
        
    st.markdown('</div>', unsafe_allow_html=True)


def _render_login_view():
    st.markdown(
        """
        <div class="login-header-logo">
            <span class="platform-title" style="font-size: 2.2rem;">SaaS Analytics</span>
        </div>
        <p class="platform-subtitle" style="margin-bottom: 20px;">Sign in to your platform account</p>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    login_method = st.radio(
        "Select Authentication Method",
        ["Email & Password", "Sign In with Google"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
    
    if login_method == "Email & Password":
        email = st.text_input("Email Address", placeholder="name@company.com", value="")
        password = st.text_input("Password", type="password", placeholder="••••••••••••")
        
        col_forgot, _ = st.columns([1, 1])
        with col_forgot:
            if st.button("Forgot Password?", key="btn_forgot_trig"):
                st.session_state.auth_page = "forgot_password"
                st.rerun()
                
        st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
        
        if st.button("Sign In", key="btn_email_login"):
            if not email or "@" not in email:
                st.error("Please enter a valid email address.")
            elif not password or len(password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                is_valid, user_name = verify_user(email, password)
                if is_valid:
                    client_details = {"ip": "127.0.0.1", "browser": "Chrome / Windows OS"}
                    smtp_conf = st.session_state.get("smtp_settings", {"demo_mode": True})
                    send_login_email_async(email, smtp_conf, client_details)
                    
                    st.success(f"Welcome back, {user_name}! Loading dashboard...")
                    time.sleep(0.8)
                    
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.error("Invalid email or password. Please try again.")
                    
    else:
        st.markdown(
            """
            <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                <div class="google-icon-wrapper" style="background-color: white; border-radius: 50%; padding: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" style="width: 48px; height: 48px;">
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
        
        if st.button("Continue with Google", key="btn_google_login"):
            creds = get_google_oauth_secrets()
            client_id = creds.get("client_id")
            redirect_uri = creds.get("redirect_uri", "http://localhost:8501")
            
            if not client_id:
                st.error("Google OAuth client ID is not configured. Please check backend/google_creds.json or Streamlit Secrets.")
            else:
                import urllib.parse
                state = "login"
                scope = "openid email profile"
                auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={client_id}&redirect_uri={urllib.parse.quote(redirect_uri)}&scope={urllib.parse.quote(scope)}&state={state}"
                
                # Execute browser redirect
                st.markdown(f"""
                    <meta http-equiv="refresh" content="0; url={auth_url}">
                    <script>window.location.href = "{auth_url}";</script>
                """, unsafe_allow_html=True)
                st.info("Redirecting to Google Sign-In...")
                st.stop()
            
    st.markdown('<div class="divider-container">or</div>', unsafe_allow_html=True)
    if st.button("Create an Account (Sign Up)", key="btn_signup_trig"):
        st.session_state.auth_page = "signup"
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)


def _render_signup_view():
    st.markdown(
        """
        <div class="login-header-logo">
            <span class="platform-title" style="font-size: 2.2rem; background: linear-gradient(135deg, #00cec9 0%, #6c5ce7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Create Account</span>
        </div>
        <p class="platform-subtitle" style="margin-bottom: 20px;">Register and configure your workspace</p>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="display: flex; justify-content: center; margin-bottom: 10px;">
            <div class="google-icon-wrapper" style="background-color: white; border-radius: 50%; padding: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
                <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" style="width: 48px; height: 48px;">
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
    
    google_su_name = st.text_input("Full Name (Display)", placeholder="Jane Doe", key="txt_google_signup_name", value="")
    
    st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)
    
    if st.button("Continue with Google", key="btn_google_signup"):
        if not google_su_name.strip():
            st.error("Please enter your display name.")
        else:
            creds = get_google_oauth_secrets()
            client_id = creds.get("client_id")
            redirect_uri = creds.get("redirect_uri", "http://localhost:8501")
            
            if not client_id:
                st.error("Google OAuth client ID is not configured. Please check backend/google_creds.json or Streamlit Secrets.")
            else:
                import urllib.parse
                username_clean = google_su_name.strip()
                state = f"signup:{username_clean}"
                scope = "openid email profile"
                auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={client_id}&redirect_uri={urllib.parse.quote(redirect_uri)}&scope={urllib.parse.quote(scope)}&state={urllib.parse.quote(state)}"
                
                # Execute browser redirect
                st.markdown(f"""
                    <meta http-equiv="refresh" content="0; url={auth_url}">
                    <script>window.location.href = "{auth_url}";</script>
                """, unsafe_allow_html=True)
                st.info("Redirecting to Google Sign-Up...")
                st.stop()
                
    st.markdown('<div class="divider-container">or register manually</div>', unsafe_allow_html=True)
    
    name = st.text_input("Full Name", placeholder="Jane Doe")
    email = st.text_input("Email Address", placeholder="name@company.com", value="")
    password = st.text_input("Password", type="password", placeholder="Minimum 6 characters")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••••••")
    
    st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
    
    if st.button("Complete Sign Up", key="btn_complete_signup"):
        if not name.strip():
            st.error("Please enter your name.")
        elif not email or "@" not in email:
            st.error("Please enter a valid email address.")
        elif not password or len(password) < 6:
            st.error("Password must be at least 6 characters.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            with st.spinner("Creating account..."):
                success, msg = register_user(name, email, password)
                time.sleep(0.8)
                
            if success:
                smtp_conf = st.session_state.get("smtp_settings", {"demo_mode": True})
                send_welcome_email_async(email, name, smtp_conf)
                
                st.success("Account successfully created!")
                time.sleep(0.8)
                
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.auth_page = "login"
                st.rerun()
            else:
                st.error(msg)
                
    st.markdown('<div style="margin-top: 20px; text-align: center;">', unsafe_allow_html=True)
    if st.button("← Back to login", key="btn_back_login_signup"):
        st.session_state.auth_page = "login"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def _render_forgot_password_view():
    st.markdown(
        """
        <div class="login-header-logo">
            <span class="platform-title" style="font-size: 2.2rem; background: linear-gradient(135deg, #00cec9 0%, #0984e3 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Reset Password</span>
        </div>
        <p class="platform-subtitle" style="margin-bottom: 20px;">Recover your platform account</p>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p style="color: #a0a0c0; font-size: 0.9rem; margin-bottom: 15px;">Enter your email below and we will send you a verification code.</p>', unsafe_allow_html=True)
    
    email = st.text_input("Email Address", placeholder="name@company.com", value="")
    st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
    
    if st.button("Send Code", key="btn_send_reset"):
        if not email or "@" not in email:
            st.error("Please enter a valid email address.")
        else:
            with st.spinner("Sending code..."):
                smtp_conf = st.session_state.get("smtp_settings", {"demo_mode": True})
                reset_token = send_password_reset_email_async(email, smtp_conf)
                time.sleep(0.8)
                
            st.session_state.reset_token = reset_token
            st.session_state.reset_email = email
            st.session_state.auth_page = "reset_password"
            st.rerun()
            
    st.markdown('<div style="margin-top: 20px; text-align: center;">', unsafe_allow_html=True)
    if st.button("← Back to login", key="btn_back_login"):
        st.session_state.auth_page = "login"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def _render_reset_password_view():
    st.markdown(
        """
        <div class="login-header-logo">
            <span class="platform-title" style="font-size: 2.2rem; background: linear-gradient(135deg, #00cec9 0%, #00b894 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">New Password</span>
        </div>
        <p class="platform-subtitle" style="margin-bottom: 20px;">Define your new account password</p>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    smtp_conf = st.session_state.get("smtp_settings", {"demo_mode": True})
    if smtp_conf.get("demo_mode", True):
        st.markdown(
            f"""
            <div class="notification-banner notification-info" style="margin-bottom: 20px;">
                🔑 <strong>Demo Mode</strong>: Enter verification code: 
                <span style="font-family: monospace; font-weight: bold; background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">
                    {st.session_state.reset_token}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="notification-banner notification-success" style="margin-bottom: 20px;">
                ✉️ A verification code has been sent to <strong>{st.session_state.reset_email}</strong>.
            </div>
            """,
            unsafe_allow_html=True
        )
        
    code_input = st.text_input("Verification Code", placeholder="SAAS-RESET-XXXXXXXX")
    new_password = st.text_input("New Password", type="password", placeholder="••••••••••••")
    confirm_password = st.text_input("Confirm New Password", type="password", placeholder="••••••••••••")
    
    st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)
    
    if st.button("Update Password", key="btn_save_password"):
        if not code_input:
            st.error("Please enter the verification code.")
        elif code_input.strip() != st.session_state.reset_token:
            st.error("Invalid verification code.")
        elif not new_password or len(new_password) < 6:
            st.error("Password must be at least 6 characters.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            st.success("Password successfully updated!")
            time.sleep(0.8)
            
            st.session_state.logged_in = True
            st.session_state.user_email = st.session_state.reset_email
            st.session_state.auth_page = "login"
            st.session_state.reset_token = None
            st.session_state.reset_email = None
            st.rerun()
            
    st.markdown('<div style="margin-top: 10px; text-align: center;">', unsafe_allow_html=True)
    if st.button("Cancel", key="btn_cancel_reset"):
        st.session_state.auth_page = "login"
        st.session_state.reset_token = None
        st.session_state.reset_email = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
