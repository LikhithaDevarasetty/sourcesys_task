import streamlit as st
import os
from datetime import datetime, timezone

# ---- Page Configuration ----
st.set_page_config(
    page_title="RupeeTracker • Personal Finance", 
    page_icon="💸", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- Load Config & Logger ----
from services.config import get_config
from services.logger import get_logger
from db.repository import Repository

logger = get_logger()

# ---- Premium Theme & UI Styling (Global Overrides) ----
if "theme" not in st.session_state:
    st.session_state.theme = get_config("app", "default_theme", default="dark")

# Custom UI Injection based on theme choice (Premium Glassmorphism & High Fidelity Contrast)
if st.session_state.theme == "dark":
    bg_color = "#07090e"
    card_bg = "rgba(13, 18, 30, 0.75)"
    text_color = "#f8fafc"
    secondary_text = "#94a3b8"
    accent_color = "#6366f1"
    accent_gradient = "linear-gradient(135deg, #6366f1, #3b82f6)"
    border_style = "1px solid rgba(255, 255, 255, 0.08)"
    shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
    glow_color = "rgba(99, 102, 241, 0.25)"
    input_bg = "rgba(255, 255, 255, 0.03)"
    active_input_border = "1px solid #6366f1"
else:
    bg_color = "#f0f2f5"
    card_bg = "rgba(255, 255, 255, 0.92)"
    text_color = "#0f172a"
    secondary_text = "#475569"
    accent_color = "#4f46e5"
    accent_gradient = "linear-gradient(135deg, #4f46e5, #06b6d4)"
    border_style = "1px solid rgba(15, 23, 42, 0.12)"
    shadow = "0 4px 24px 0 rgba(31, 38, 135, 0.10)"
    glow_color = "rgba(79, 70, 229, 0.18)"
    input_bg = "rgba(0, 0, 0, 0.03)"
    active_input_border = "1px solid #4f46e5"

# Dynamically set Streamlit's internal theme so dataframes/canvas widgets match
try:
    if st.session_state.theme == "dark":
        st._config.set_option("theme.base", "dark")
        st._config.set_option("theme.backgroundColor", "#07090e")
        st._config.set_option("theme.secondaryBackgroundColor", "#0d121e")
        st._config.set_option("theme.textColor", "#f8fafc")
        st._config.set_option("theme.primaryColor", "#6366f1")
    else:
        st._config.set_option("theme.base", "light")
        st._config.set_option("theme.backgroundColor", "#f0f2f5")
        st._config.set_option("theme.secondaryBackgroundColor", "#ffffff")
        st._config.set_option("theme.textColor", "#0f172a")
        st._config.set_option("theme.primaryColor", "#4f46e5")
except Exception:
    pass  # Graceful fallback if st._config is not available

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* ---- Keyframe Animations ---- */
    @keyframes appFadeIn {{
        from {{ opacity: 0; transform: translateY(16px); filter: blur(4px); }}
        to {{ opacity: 1; transform: translateY(0); filter: blur(0); }}
    }}
    
    @keyframes alertSlideIn {{
        from {{ opacity: 0; transform: scale(0.96) translateY(-15px); }}
        to {{ opacity: 1; transform: scale(1) translateY(0); }}
    }}

    @keyframes pulseGlow {{
        0% {{ box-shadow: 0 0 0 0 {glow_color}; }}
        70% {{ box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }}
    }}

    /* ===== FORCE ALL STREAMLIT CONTAINERS TO MATCH THEME ===== */
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main,
    [data-testid="stMainBlockContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"],
    .block-container {{
        background-color: {bg_color} !important;
    }}

    /* Global App Canvas Fade-in Animation */
    [data-testid="stAppViewContainer"] {{
        animation: appFadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
    }}
    
    /* App-wide Typography */
    html, body, [data-testid="stAppViewContainer"], .main {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: {text_color} !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: {text_color} !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }}

    /* High Specificity Typography & Widget Label Overrides for Perfect Theme Adaptability */
    label[data-testid="stWidgetLabel"],
    label[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] span,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stMarkdownContainer"] a,
    [data-testid="stMarkdownContainer"] code,
    [data-testid="stCaptionContainer"] p,
    [data-testid="stCaptionContainer"] span,
    [data-testid="stRadio"] label,
    [data-testid="stRadio"] label p,
    [data-testid="stRadio"] div[role="radiogroup"] label,
    [data-testid="stRadio"] div[role="radiogroup"] label p,
    [data-testid="stRadio"] div[role="radiogroup"] label div,
    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] label p,
    [data-testid="stCheckbox"] label span {{
        color: {text_color} !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}

    /* Caption muted text */
    [data-testid="stCaptionContainer"] p {{
        color: {secondary_text} !important;
    }}

    /* Inline code blocks */
    [data-testid="stMarkdownContainer"] code {{
        background-color: {input_bg} !important;
        border: {border_style} !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
    }}
    
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}

    /* Global Input Placeholders */
    ::placeholder {{
        color: {secondary_text} !important;
        opacity: 0.7 !important;
    }}

    /* Streamlit Native Metric Visual Harmony overrides */
    [data-testid="stMetricValue"] {{
        color: {text_color} !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {secondary_text} !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-size: 11px !important;
    }}
    [data-testid="stMetricDelta"] {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}

    /* Select box value text */
    div[data-testid="stSelectbox"] div[role="combobox"] span,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] div {{
        color: {text_color} !important;
    }}

    /* Number input +/- spinner buttons */
    div[data-testid="stNumberInput"] button {{
        color: {text_color} !important;
        background-color: {input_bg} !important;
        border: {border_style} !important;
    }}
    div[data-testid="stNumberInput"] button:hover {{
        background-color: {accent_color}22 !important;
        color: {accent_color} !important;
    }}

    /* Date input internal text */
    div[data-testid="stDateInput"] input {{
        background-color: {input_bg} !important;
        border: {border_style} !important;
        border-radius: 12px !important;
        color: {text_color} !important;
        padding: 10px 14px !important;
        transition: all 0.3s ease !important;
    }}
    div[data-testid="stDateInput"] input:focus {{
        border: {active_input_border} !important;
        box-shadow: {glow_color} 0px 0px 12px !important;
    }}
    div[data-testid="stDateInput"] button {{
        color: {text_color} !important;
    }}

    /* Premium Portal Dropdowns (Uber Baseweb Popovers & Calendars) */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] ul,
    ul[role="listbox"],
    div[data-baseweb="calendar"] {{
        background-color: {bg_color} !important;
        backdrop-filter: blur(16px) !important;
        border: {border_style} !important;
        border-radius: 12px !important;
        box-shadow: {shadow} !important;
    }}
    div[data-baseweb="popover"] li,
    ul[role="listbox"] li[role="option"],
    div[data-baseweb="calendar"] button {{
        color: {text_color} !important;
        background-color: transparent !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 14px !important;
        padding: 8px 12px !important;
        transition: all 0.2s ease !important;
    }}
    div[data-baseweb="popover"] li:hover,
    ul[role="listbox"] li[role="option"]:hover,
    div[data-baseweb="popover"] li[aria-selected="true"],
    ul[role="listbox"] li[role="option"][aria-selected="true"],
    div[data-baseweb="calendar"] button:hover {{
        background-color: {accent_color}22 !important;
        color: {accent_color} !important;
    }}
    div[data-baseweb="calendar"] button[aria-selected="true"] {{
        background-color: {accent_color} !important;
        color: #ffffff !important;
    }}
    /* Calendar month/year header text */
    div[data-baseweb="calendar"] div,
    div[data-baseweb="calendar"] span {{
        color: {text_color} !important;
    }}

    /* Slider styling */
    [data-testid="stSlider"] label p,
    [data-testid="stSlider"] div[data-testid="stThumbValue"] {{
        color: {text_color} !important;
    }}
    [data-testid="stSlider"] div[role="slider"] {{
        background-color: {accent_color} !important;
    }}

    /* Progress bar track */
    [data-testid="stProgress"] > div {{
        background-color: {input_bg} !important;
        border-radius: 8px !important;
    }}

    /* Dataframe table header and cells */
    [data-testid="stDataFrame"] {{
        border: {border_style} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }}

    /* Toast notifications */
    div[data-testid="stToast"] {{
        background: {card_bg} !important;
        backdrop-filter: blur(12px) !important;
        border: {border_style} !important;
        border-radius: 12px !important;
        color: {text_color} !important;
        box-shadow: {shadow} !important;
    }}
    div[data-testid="stToast"] p,
    div[data-testid="stToast"] span {{
        color: {text_color} !important;
    }}

    /* Expander styling */
    [data-testid="stExpander"] {{
        background: {card_bg} !important;
        border: {border_style} !important;
        border-radius: 12px !important;
        box-shadow: {shadow} !important;
    }}
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary p {{
        color: {text_color} !important;
    }}

    /* Sidebar toggle (hamburger) button */
    button[data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebar"] button[data-testid="stSidebarNavCollapseIcon"],
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {{
        color: {text_color} !important;
    }}
    button[data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stSidebar"] button svg {{
        fill: {text_color} !important;
        stroke: {text_color} !important;
    }}

    /* Main block container background */
    .main .block-container {{
        background-color: transparent !important;
    }}

    /* Notification text children */
    [data-testid="stNotification"] p,
    [data-testid="stNotification"] span,
    [data-testid="stNotification"] strong,
    [data-testid="stNotification"] a {{
        color: {text_color} !important;
    }}

    /* Spinner text */
    .stSpinner > div {{
        color: {text_color} !important;
    }}

    /* Multiselect tags */
    span[data-baseweb="tag"] {{
        background-color: {accent_color}22 !important;
        color: {accent_color} !important;
        border-radius: 8px !important;
    }}
    span[data-baseweb="tag"] span {{
        color: {accent_color} !important;
    }}
    
    /* Metric Cards Transitions & Animations */
    .finance-card {{
        background: {card_bg} !important;
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        padding: 24px;
        border-radius: 20px !important;
        border: {border_style} !important;
        box-shadow: {shadow} !important;
        margin-bottom: 18px;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .finance-card:hover {{
        transform: translateY(-6px) scale(1.015);
        border-color: {accent_color} !important;
        box-shadow: {glow_color} 0px 12px 30px, rgba(0,0,0,0.1) 0px 4px 10px !important;
    }}
    .card-label {{
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {secondary_text};
        font-weight: 700;
        margin-bottom: 8px;
    }}
    .card-value {{
        font-size: 32px;
        font-weight: 800;
        color: {text_color};
        letter-spacing: -0.03em;
    }}
    .card-footer {{
        font-size: 12px;
        color: {secondary_text};
        margin-top: 10px;
        font-weight: 500;
    }}
    
    /* High Contrast Glassmorphic Forms */
    div[data-testid="stForm"] {{
        background: {card_bg} !important;
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border-radius: 20px !important;
        border: {border_style} !important;
        padding: 30px !important;
        box-shadow: {shadow} !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    div[data-testid="stForm"]:focus-within {{
        border-color: {accent_color} !important;
        box-shadow: {glow_color} 0px 0px 24px, {shadow} !important;
    }}
    
    /* Styled Input Fields (Glass inputs) */
    div[data-testid="stTextInput"] input, 
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stSelectbox"] div[role="combobox"] {{
        background-color: {input_bg} !important;
        border: {border_style} !important;
        border-radius: 12px !important;
        color: {text_color} !important;
        padding: 10px 14px !important;
        transition: all 0.3s ease !important;
    }}
    div[data-testid="stTextInput"] input:focus, 
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {{
        border: {active_input_border} !important;
        box-shadow: {glow_color} 0px 0px 12px !important;
    }}
    
    /* Premium iOS-style segmented navigation */
    div[data-testid="stPills"] {{
        background: {card_bg} !important;
        padding: 6px !important;
        border-radius: 9999px !important;
        border: {border_style} !important;
        box-shadow: {shadow} !important;
        backdrop-filter: blur(16px) saturate(180%);
        gap: 4px !important;
    }}
    div[data-testid="stPills"] button {{
        background-color: transparent !important;
        border: none !important;
        border-radius: 9999px !important;
        color: {secondary_text} !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
        font-size: 14px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    div[data-testid="stPills"] button[aria-selected="true"] {{
        background: {accent_gradient} !important;
        color: #ffffff !important;
        box-shadow: {glow_color} 0px 4px 12px !important;
    }}
    div[data-testid="stPills"] button:hover {{
        color: {text_color} !important;
        transform: translateY(-1px);
    }}
    
    /* Buttons Customization (Gradient fill for primary actions) */
    .stButton>button {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: {border_style} !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        box-shadow: {shadow} !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    .stButton>button:hover {{
        border-color: {accent_color} !important;
        color: {accent_color} !important;
        transform: translateY(-2px);
        box-shadow: {glow_color} 0px 6px 15px !important;
    }}
    .stButton>button:active {{
        transform: translateY(1px);
    }}
    
    /* Special Primary Buttons (Form submissions) */
    div[data-testid="stForm"] button[type="submit"],
    div[data-testid="stFormSubmitButton"] button,
    button.st-emotion-cache-19rxjzo {{
        background: {accent_gradient} !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        box-shadow: {glow_color} 0px 4px 16px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    div[data-testid="stForm"] button[type="submit"]:hover {{
        transform: translateY(-2px);
        box-shadow: {glow_color} 0px 8px 24px, rgba(0,0,0,0.15) 0px 4px 10px !important;
    }}

    /* Global Status Notifications Slide/Fade Dropdown Animation */
    [data-testid="stNotification"] {{
        background: {card_bg} !important;
        backdrop-filter: blur(12px) !important;
        border: {border_style} !important;
        border-radius: 16px !important;
        box-shadow: {shadow} !important;
        color: {text_color} !important;
        animation: alertSlideIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.1) both;
    }}
    
    /* Styled HR */
    hr {{
        margin: 2rem 0 !important;
        border: 0;
        border-top: {border_style};
    }}
    
    /* ---- Sidebar Custom Styling ---- */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"],
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    [data-testid="stSidebar"] {{
        border-right: {border_style} !important;
    }}
    [data-testid="stSidebar"] [data-testid="stForm"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
    }}
    .sidebar-profile-card {{
        background: {card_bg} !important;
        backdrop-filter: blur(12px) saturate(180%);
        -webkit-backdrop-filter: blur(12px) saturate(180%);
        padding: 16px;
        border-radius: 16px !important;
        border: {border_style} !important;
        margin-bottom: 20px;
        box-shadow: {shadow} !important;
    }}
    [data-testid="stSidebar"] div[data-testid="stPills"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
    }}
    [data-testid="stSidebar"] div[data-testid="stPills"] button {{
        background-color: {card_bg} !important;
        border: {border_style} !important;
        border-radius: 12px !important;
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
        box-shadow: {shadow} !important;
        padding: 10px 16px !important;
        color: {text_color} !important;
    }}
    [data-testid="stSidebar"] div[data-testid="stPills"] button[aria-selected="true"] {{
        background: {accent_gradient} !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: {glow_color} 0px 4px 12px !important;
    }}

    /* ---- Dataframe / Table full theme override ---- */
    [data-testid="stDataFrame"] iframe {{
        border-radius: 12px !important;
    }}
    /* Override glide-data-grid (Streamlit's internal table renderer) */
    [data-testid="stDataFrame"] [role="grid"],
    [data-testid="stDataFrame"] [data-testid="glideDataEditor"],
    [data-testid="stDataFrame"] canvas {{
        border-radius: 12px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Accessibility announcer for screen readers
st.markdown('<div id="a11y-announcer" aria-live="polite" style="position:absolute;left:-9999px"></div>', unsafe_allow_html=True)

# ---- Database Setup ----
database_url = get_config("database", "url", default="sqlite:///finance_app.db")
repo = Repository(database_url)
repo.init()

# Seed default categories
try:
    from db.seed import seed_default_categories
    seed_default_categories(repo)
except Exception as e:
    logger.warning(f"Category setup status: {e}")

# Auto-seed demo user on first startup (ensures demo data exists on deployment)
if "demo_seeded" not in st.session_state:
    st.session_state.demo_seeded = True
    try:
        demo_email = "demo@rupeetracker.com"
        existing_demo = repo.get_user_by_email(demo_email)
        needs_seed = False
        if not existing_demo:
            needs_seed = True
        else:
            # Also re-seed if user exists but has no transactions (failed previous seed)
            txs = repo.list_transactions_for_user(existing_demo.id, limit=1)
            if not txs:
                needs_seed = True
        if needs_seed:
            logger.info("Demo user missing or empty — auto-seeding demo data...")
            from seed_demo_user import seed_demo_user
            seed_demo_user()
            logger.info("Demo user auto-seeded successfully.")
    except Exception as e:
        logger.warning(f"Demo auto-seed skipped: {e}")

# ---- Authentication Infrastructure ----
from services.auth import create_token, decode_token, token_expired
from services.auth import create_action_token, verify_action_token
from services.passwords import verify_password
from services.user_service import create_user, authenticate
from sqlalchemy.exc import IntegrityError
from services.emailer import send_login_email, send_logout_email

if "jwt" not in st.session_state:
    st.session_state.jwt = None

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

def current_user_email() -> str | None:
    token = st.session_state.jwt
    if not token:
        return None
    try:
        if token_expired(token):
            return None
        payload = decode_token(token)
        return payload.get("email")
    except Exception:
        return None

user_email = current_user_email()

# ---- Application Header ----
st.title("RupeeTracker")
st.caption("Track your daily income, monthly spending, investments, and budgets easily.")

# ---- Authentication Views Layout (Tabs are completely hidden here) ----
if not user_email:
    # Handle password reset via token in query params
    try:
        qp = st.experimental_get_query_params()
        if "reset_token" in qp:
            token = qp.get("reset_token")[0]
            payload = verify_action_token(token, "password_reset")
            if not payload:
                st.error("Password reset link is invalid or has expired.")
                if st.button("Request a new reset link"):
                    st.session_state.auth_mode = "forgot"
                    st.experimental_set_query_params()
                    st.rerun()
                st.stop()

            # Valid token: show set-new-password form
            st.subheader("Set a new password")
            st.caption("Enter a new secure password for your account.")
            with st.form("reset_complete_form", clear_on_submit=False):
                npw = st.text_input("New password", type="password", placeholder="Minimum 8 characters")
                npw2 = st.text_input("Confirm new password", type="password", placeholder="Retype password")
                submit_reset_complete = st.form_submit_button("Set new password", use_container_width=True)

            if submit_reset_complete:
                if not npw or len(npw) < 8:
                    st.error("Password must be at least 8 characters long.")
                elif npw != npw2:
                    st.error("Passwords do not match.")
                else:
                    email_for = payload.get("email")
                    user_obj = repo.get_user_by_email(email_for)
                    from services.passwords import hash_password
                    if user_obj:
                        new_hash = hash_password(npw)
                        ok = repo.set_user_password(user_obj.id, new_hash)
                        try:
                            from services.emailer import send_email
                            send_email(user_obj.email, "Your password was changed — RupeeTracker", f"Hi {user_obj.email},\n\nYour account password was successfully changed. If you did not perform this action, contact support immediately.")
                        except Exception:
                            logger.warning("Failed to send password-change notification to %s", user_obj.email, exc_info=True)
                        if ok:
                            st.success("Password updated successfully — you can now log in.")
                            st.experimental_set_query_params()
                            st.rerun()
                        else:
                            st.error("Failed to update password. Try again later.")
                    else:
                        # Do not reveal account existence
                        st.success("If your account exists, the password has been updated. You can now log in.")
                        st.experimental_set_query_params()
                        st.rerun()
            st.stop()

    except Exception:
        pass

    _, auth_col, _ = st.columns([1, 1.8, 1])
    with auth_col:
        if st.session_state.auth_mode == "login":
            st.subheader("Login to Your Account")
            st.caption("Secure access to your personal finance records.")
            with st.form("auth_form", clear_on_submit=False):
                email = st.text_input("Email Address", placeholder="name@email.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                submit = st.form_submit_button("Login", use_container_width=True)

            if submit:
                import re
                if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error("Please enter a valid email address.")
                elif not password or len(password) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    user = repo.get_user_by_email(email)
                    if not user or not verify_password(password, user.password_hash):
                        st.error("Incorrect email or password.")
                    else:
                        st.session_state.jwt = create_token(user.id, user.email)
                        try:
                            send_login_email(user.email, user.email)
                        except Exception as e:
                            logger.warning("Notification delay: %s", e)
                        st.success("Log in successful!")
                        st.rerun()

            st.markdown("<br/>", unsafe_allow_html=True)
            b_col1, b_col2 = st.columns(2)
            if b_col1.button("Create a fresh new account", use_container_width=True):
                st.session_state.auth_mode = "signup"
                st.rerun()
            if b_col2.button("Forgot Password?", use_container_width=True):
                st.session_state.auth_mode = "forgot"
                st.rerun()

        elif st.session_state.auth_mode == "signup":
            st.subheader("Create a New Account")
            st.caption("Start keeping your financial logs safe and local.")
            with st.form("auth_form", clear_on_submit=False):
                email = st.text_input("Email Address", placeholder="name@email.com")
                password = st.text_input("Choose Password", type="password", placeholder="Minimum 8 characters")
                submit = st.form_submit_button("Register Account", use_container_width=True)

            if submit:
                import re
                if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error("Please enter a valid email address.")
                elif not password or len(password) < 8:
                    st.error("Your password must be at least 8 characters long.")
                else:
                    existing = repo.get_user_by_email(email)
                    if existing:
                        st.error("This email is already registered.")
                    else:
                        try:
                            create_user(repo, email, password)
                            user = repo.get_user_by_email(email)
                            st.success("Account created successfully!")
                            st.session_state.jwt = create_token(user.id, user.email)
                            try:
                                send_login_email(user.email, user.email)
                            except Exception as e:
                                logger.warning("Sign up email failed: %s", e)
                            st.rerun()
                        except IntegrityError:
                            st.error("This email is already taken.")
                        except Exception as e:
                            logger.warning("Account creation error: %s", e)
                            st.error("Could not register. Please try again.")

            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("Back to login screen", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()
                
        elif st.session_state.auth_mode == "forgot":
            st.subheader("Reset Your Password")
            st.caption("Enter your registered email below to receive a secure reset code via email.")
            with st.form("forgot_password_form", clear_on_submit=False):
                reset_email = st.text_input("Registered Email Address", placeholder="name@email.com")
                submit_reset = st.form_submit_button("Send Reset Code", use_container_width=True)

            if submit_reset:
                if not reset_email:
                    st.error("Please fill in your email address.")
                else:
                    # Generate a one-time numeric code and email it; for security, do not reveal existence
                    try:
                        user_obj = repo.get_user_by_email(reset_email)
                        code = None
                        if user_obj:
                            import random
                            code = f"{random.randint(100000,999999)}"
                            pr = repo.create_password_reset(reset_email, code, ttl_minutes=20)
                            from services.emailer import send_reset_code_email
                            try:
                                send_reset_code_email(reset_email, code, ttl_minutes=20)
                            except Exception:
                                logger.warning("Failed to send reset code email to %s", reset_email, exc_info=True)

                        # Always show generic response regardless of account existence
                        st.success("If an account exists for that email, we've sent a reset code. Check your email.")
                        # store email in session to allow immediate code entry UI
                        st.session_state.reset_email = reset_email
                        st.session_state.reset_code_sent = True

                    except Exception as e:
                        logger.exception("Failed to queue reset code: %s", e)
                        st.error("Failed to process reset request. Try again later.")

            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("Back to login screen", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()

            # If a reset code was sent, show the code entry + new password form
            if st.session_state.get("reset_code_sent") and st.session_state.get("reset_email"):
                st.markdown("---")
                st.subheader("Enter reset code")
                with st.form("enter_code_form", clear_on_submit=False):
                    code_entered = st.text_input("Enter code from email", placeholder="123456")
                    new_pw = st.text_input("New password", type="password", placeholder="Minimum 8 characters")
                    new_pw2 = st.text_input("Confirm new password", type="password", placeholder="Retype password")
                    submit_code = st.form_submit_button("Set new password", use_container_width=True)

                if submit_code:
                    if not code_entered:
                        st.error("Enter the code you received by email.")
                    elif not new_pw or len(new_pw) < 8:
                        st.error("Provide a new password at least 8 characters long.")
                    elif new_pw != new_pw2:
                        st.error("Passwords do not match.")
                    else:
                        # validate code
                        pr = repo.get_password_reset_by_email_code(st.session_state.reset_email, code_entered)
                        if not pr:
                            st.error("Invalid or expired code. Request a new code if needed.")
                        else:
                            from services.passwords import hash_password
                            new_hash = hash_password(new_pw)
                            # update password if user exists
                            user_obj = repo.get_user_by_email(st.session_state.reset_email)
                            if user_obj:
                                ok = repo.set_user_password(user_obj.id, new_hash)
                                repo.mark_password_reset_used(pr.id)
                                try:
                                    from services.emailer import send_email
                                    send_email(user_obj.email, "Password changed — RupeeTracker", f"Hi {user_obj.email},\n\nYour password was changed via the reset code. If you did not perform this action contact support.")
                                except Exception:
                                    logger.warning("Failed to send password-change notification to %s", user_obj.email, exc_info=True)
                                if ok:
                                    st.success("Password updated. Please log in with your new password.")
                                    # clear session reset flags
                                    del st.session_state["reset_code_sent"]
                                    del st.session_state["reset_email"]
                                    st.session_state.auth_mode = "login"
                                    st.rerun()
                                else:
                                    st.error("Failed to update password; try again later.")
                            else:
                                # should not happen (we only created code for existing users), but handle gracefully
                                st.success("If your account exists, the password has been updated. You can now log in.")
                                del st.session_state["reset_code_sent"]
                                del st.session_state["reset_email"]
                                st.session_state.auth_mode = "login"
                                st.rerun()
    st.stop()

# ---- Post-Authentication State Setup (Show Navigation Tabs & Menus Only Now) ----
page_options = ["Home Dashboard", "Add Money Entry", "Spending Analytics", "Monthly Budgets", "Future Forecast", "Manage Categories"]
page = "Home Dashboard"

try:
    params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
    if "page" in params:
        qpage = params["page"][0] if isinstance(params["page"], list) else params["page"]
        if qpage in page_options:
            page = qpage
except Exception:
    pass

# Keyboard shortcuts Script injection
shortcut_bg = "rgba(15, 23, 42, 0.85)" if st.session_state.theme == "dark" else "rgba(255, 255, 255, 0.92)"
shortcut_text = "#ffffff" if st.session_state.theme == "dark" else "#0f172a"
shortcut_border = "1px solid rgba(255,255,255,0.1)" if st.session_state.theme == "dark" else "1px solid rgba(15, 23, 42, 0.12)"
shortcut_shadow = "none" if st.session_state.theme == "dark" else "0 2px 8px rgba(0,0,0,0.08)"
st.markdown(
    f"""
    <script>
    function setPage(p){{ const params=new URLSearchParams(window.location.search); params.set('page',p); window.history.replaceState({{}},'',`${{location.pathname}}?${{params}}`); }}
    document.addEventListener('keydown', function(e) {{
        const tag = document.activeElement && document.activeElement.tagName;
        if(tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
        if (e.key === 'n') {{ setPage('Add Money Entry'); location.reload(); }}
        if (e.key === 'd') {{ setPage('Home Dashboard'); location.reload(); }}
        if (e.key === 'e') {{ setPage('Spending Analytics'); location.reload(); }}
    }});
    </script>
    <style>
    .shortcut-help {{position: fixed; bottom: 16px; right: 16px; background: {shortcut_bg}; backdrop-filter: blur(8px); color: {shortcut_text}; padding: 6px 14px; border-radius: 9999px; font-size: 12px; border: {shortcut_border}; box-shadow: {shortcut_shadow}; z-index: 999;}}
    </style>
    <div class="shortcut-help" role="status" aria-hidden="false">⚡ Shortcuts Active</div>
    """,
    unsafe_allow_html=True,
)

# ---- Sidebar Navigation & Controls (Visible post-login) ----
user = repo.get_user_by_email(user_email)

with st.sidebar:
    # Branding Section
    st.markdown(
        f"""
        <div style="background: {accent_gradient}; padding: 20px; border-radius: 16px; margin-bottom: 20px; text-align: center; box-shadow: {shadow};">
            <h2 style="color: #ffffff !important; margin: 0; font-size: 22px; font-weight: 800;">💸 RupeeTracker</h2>
            <div style="color: rgba(255, 255, 255, 0.8); font-size: 11px; margin-top: 4px; font-weight: 500;">PREMIUM WEALTH COMPANION</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Profile Card
    if user:
        st.markdown(
            f"""
            <div class="sidebar-profile-card">
                <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: {secondary_text}; font-weight: 700; margin-bottom: 4px;">Active Profile</div>
                <div style="font-size: 14px; font-weight: 700; color: {text_color}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{user_email}">{user_email}</div>
                <div style="font-size: 11px; color: {secondary_text}; margin-top: 4px;">User ID: #{user.id}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Sidebar Navigation Option selection
    st.markdown(f"<div style='font-size: 12px; font-weight: 700; color: {secondary_text}; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;'>Navigation</div>", unsafe_allow_html=True)
    page = st.pills(
        label="Navigation Menu",
        options=page_options,
        selection_mode="single",
        default=page,
        label_visibility="collapsed",
        key="sidebar_navigation"
    )
    if not page:
        page = "Home Dashboard"
        
    st.markdown("<hr style='margin: 15px 0 !important;' />", unsafe_allow_html=True)
    
    # Theme Selection
    st.markdown(f"<div style='font-size: 12px; font-weight: 700; color: {secondary_text}; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;'>App Theme</div>", unsafe_allow_html=True)
    theme_choice = st.radio(
        "Display Mode", 
        ["dark", "light"], 
        index=0 if st.session_state.theme == "dark" else 1, 
        horizontal=True,
        label_visibility="collapsed",
        key="sidebar_theme_selector"
    )
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()
        
    st.markdown("<hr style='margin: 15px 0 !important;' />", unsafe_allow_html=True)
    
    # Sandbox Seeder Control
    st.markdown(f"<div style='font-size: 12px; font-weight: 700; color: {secondary_text}; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;'>Quick Controls</div>", unsafe_allow_html=True)
    if st.button("🔄 Reset & Seed Demo Data", use_container_width=True, key="sandbox_seeder_button"):
        with st.spinner("Seeding database..."):
            try:
                from seed_demo_user import seed_demo_user
                seed_demo_user()
                st.toast("Database seeded successfully!", icon="🔄")
                st.success("Successfully seeded demo user database!")
                st.rerun()
            except Exception as e:
                st.error(f"Seeder failed: {e}")
                
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    # Sign Out Button
    if st.button("🚪 Sign Out", use_container_width=True, type="secondary", key="sidebar_signout_button"):
        try:
            payload = decode_token(st.session_state.jwt)
            send_logout_email(payload.get("email"), payload.get("email"))
        except Exception as e:
            logger.warning("Logout email delay: %s", e)
        st.session_state.jwt = None
        st.rerun()

st.markdown("<hr/>", unsafe_allow_html=True)

# ---- Global Budget Notification Checks ----
if user:
    from services.budgets import evaluate_budgets
    from services.emailer import send_budget_warning_email, send_budget_breach_email
    try:
        active_budgets = evaluate_budgets(repo, user.id)
        for b in active_budgets:
            if b["category_id"] is None:
                label_name = "Overall Dashboard Budget"
            else:
                cats = repo.list_categories(user.id)
                label_name = next((c.name for c in cats if c.id == b["category_id"]), "Category Group")
            
            # Budget Notification Render (existing UI banners — unchanged)
            if b["ratio"] >= 1.0:
                st.error(f"🚨 **Critical Budget Alert!** You have breached your maximum limit for **{label_name}**. (Spent ₹{b['spent']:,.2f} of ₹{b['limit']:,.2f})")
            elif b["ratio"] >= 0.8:
                st.warning(f"⚠️ **Warning Alert!** You have consumed **{int(b['ratio']*100)}%** of your allowed budget cap for **{label_name}**.")
            else:
                st.success(f"✅ **Budget Safe!** Your spending for **{label_name}** is well within limits. (Spent ₹{b['spent']:,.2f} out of ₹{b['limit']:,.2f})")

            # Budget Email Alerts (sent once per session per budget per status)
            email_flag_key = f"budget_email_sent_{b['id']}_{b['status']}"
            if email_flag_key not in st.session_state:
                st.session_state[email_flag_key] = True
                try:
                    if b["status"] == "red":
                        over_amount = b["spent"] - b["limit"]
                        send_budget_breach_email(user_email, label_name, b["spent"], b["limit"], over_amount)
                        logger.info("Budget breach email sent for '%s' to %s", label_name, user_email)
                    elif b["status"] == "orange":
                        send_budget_warning_email(user_email, label_name, b["spent"], b["limit"], int(b["ratio"] * 100))
                        logger.info("Budget warning email sent for '%s' to %s", label_name, user_email)
                except Exception as e:
                    logger.warning("Budget alert email failed for '%s': %s", label_name, e)
    except Exception as e:
        logger.warning(f"Budget evaluator scanner trace issue: {e}")

st.markdown("<br/>", unsafe_allow_html=True)

# ---- Page Routing Views Architecture ----
if page == "Home Dashboard":
    st.subheader("Monthly Money Dashboard")
    st.caption("A summary overview of your income, expenses, and savings for this month.")

    if not user:
        st.error("Session sync failed. Please log in again.")
    else:
        import pandas as pd
        from services.analytics import monthly_totals, category_totals_for_month

        # ---- Dashboard Hero Block ----
        current_hour = datetime.now().hour
        if current_hour < 12:
            greeting = "Good Morning"
        elif current_hour < 17:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
            
        greeting_user = "Demo User" if user_email == "demo@rupeetracker.com" else user_email.split('@')[0]
        greeting_text = f"{greeting}, {greeting_user}! 👋"
        
        finance_tips = [
            "Track every expense, no matter how small. Little leaks can sink a big ship.",
            "Pay yourself first: aim to save at least 20% of your income before spending.",
            "An investment in knowledge pays the best interest. Spend time reading about personal finance.",
            "Separate your wants from your needs to avoid impulse purchases.",
            "Keep an emergency fund with 3-6 months of living expenses in a liquid account.",
            "Review your subscriptions regularly. Cancel what you don't use.",
            "Compound interest is the eighth wonder of the world. He who understands it, earns it; he who doesn't, pays it.",
            "Inflation is a quiet thief. Invest in assets that grow faster than inflation.",
            "A budget is telling your money where to go instead of wondering where it went."
        ]
        day_of_year = datetime.now().timetuple().tm_yday
        tip_of_the_day = finance_tips[day_of_year % len(finance_tips)]

        mt = monthly_totals(repo, user.id, months=3)
        if mt.empty:
            income = 0.0
            expense = 0.0
        else:
            latest = mt.tail(1).iloc[0]
            income = latest.income
            expense = latest.expense

        if income == 0 and expense == 0:
            cashflow_status = "No transactions yet"
            status_color = "#94a3b8"
            ratio_percent = 0
        elif income == 0:
            cashflow_status = "Deficit Danger"
            status_color = "#EF4444"
            ratio_percent = 100
        else:
            ratio = expense / income
            ratio_percent = int(ratio * 100)
            if ratio < 0.5:
                cashflow_status = "High Surplus"
                status_color = "#10B981"
            elif ratio <= 0.8:
                cashflow_status = "Balanced"
                status_color = "#F59E0B"
            else:
                cashflow_status = "Deficit Danger"
                status_color = "#EF4444"

        st.markdown(
            f"""
            <div style="background: {card_bg}; border-left: 6px solid {accent_color}; padding: 24px; border-radius: 16px; margin-bottom: 24px; box-shadow: {shadow};">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                    <div>
                        <h2 style="margin: 0; font-size: 24px; color: {text_color};">{greeting_text}</h2>
                        <p style="margin: 6px 0 0 0; font-size: 14px; color: {secondary_text}; font-style: italic;">" {tip_of_the_day} "</p>
                    </div>
                    <div style="background: {input_bg}; padding: 12px 20px; border-radius: 12px; border: {border_style}; min-width: 180px;">
                        <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: {secondary_text}; font-weight: 700; margin-bottom: 4px;">Cash Flow Health</div>
                        <span style="background-color: {status_color}22; color: {status_color}; padding: 4px 8px; border-radius: 6px; font-size: 12px; font-weight: 700; border: 1px solid {status_color}44;">{cashflow_status}</span>
                        <div style="font-size: 12px; color: {secondary_text}; margin-top: 6px;">Spent: {ratio_percent}% of earnings</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if mt.empty:
            st.info("No logs found yet. Click 'Add Money Entry' to put in your salary, bills, or investments!")
        else:
            latest = mt.tail(1).iloc[0]
            avg_expense = mt["expense"].mean() if "expense" in mt.columns else 0.0
            
            # Simplified Financial Cards
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.markdown(f"""
                    <div class="finance-card" role="region" tabindex="0" aria-label="Total Money Earned">
                        <div class="card-label">Total Earnings / Income</div>
                        <div class="card-value" style="color: #10B981;">₹{latest.income:,.2f}</div>
                        <div class="card-footer">Salary, business payments & collections</div>
                    </div>
                """, unsafe_allow_html=True)
            with m_col2:
                st.markdown(f"""
                    <div class="finance-card" role="region" tabindex="0" aria-label="Total Money Spent">
                        <div class="card-label">Total Spending / Expenses</div>
                        <div class="card-value" style="color: #EF4444;">₹{latest.expense:,.2f}</div>
                        <div class="card-footer">Rent, bills, EMIs, grocery & shopping expenses</div>
                    </div>
                """, unsafe_allow_html=True)
            with m_col3:
                net_val = latest.income - latest.expense
                net_color = "#10B981" if net_val >= 0 else "#EF4444"
                st.markdown(f"""
                    <div class="finance-card" role="region" tabindex="0" aria-label="Net Balance Left Over">
                        <div class="card-label">Net Savings Left</div>
                        <div class="card-value" style="color: {net_color};">₹{net_val:,.2f}</div>
                        <div class="card-footer">Surplus funds left in your bank account</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<br/>", unsafe_allow_html=True)
            scols = st.columns([1, 1, 1])
            scols[0].metric("Average Monthly Spending", f"₹{avg_expense:,.2f}")
            try:
                ct = category_totals_for_month(repo, user.id, latest.month.year, latest.month.month)
                top_cat = ct.sort_values(by="expense", ascending=False).iloc[0]["category"] if (not ct.empty and "expense" in ct.columns) else "None"
            except Exception:
                top_cat = "None"
            scols[1].metric("Biggest Spending Group", top_cat)
            
            with scols[2]:
                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                if st.button("➕ Log a New Transaction", use_container_width=True):
                    st.query_params = {"page": "Add Money Entry"} if hasattr(st, "query_params") else st.experimental_set_query_params(page=["Add Money Entry"])
                    st.rerun()

        st.markdown("---")
        st.subheader("Your Money Passbook History")
        
        try:
            # Fetch all transactions for live memory-based search/filtering (capped at 10000)
            all_txs = repo.list_transactions_for_user(user.id, limit=10000)
            if not all_txs:
                st.info("Passbook history is blank. Click 'Add Money Entry' or seed data in the sidebar to populate records.")
            else:
                # 3 columns for search, category filter, and type pills
                f_col1, f_col2, f_col3 = st.columns(3)
                
                with f_col1:
                    search_query = st.text_input("🔍 Search Description", placeholder="Type notes or remarks...")
                    
                with f_col2:
                    unique_categories = sorted(list(set(t.category_or_source for t in all_txs if t.category_or_source)))
                    category_filter = st.selectbox("Category Filter", ["All Categories"] + unique_categories)
                    
                with f_col3:
                    type_filter = st.pills(
                        "Transaction Type", 
                        ["All Types", "INCOME", "EXPENSE"], 
                        selection_mode="single", 
                        default="All Types",
                        key="passbook_type_pills"
                    )
                    if not type_filter:
                        type_filter = "All Types"

                # Filter rows dynamically in memory
                rows = []
                for t in all_txs:
                    # Match Search Query
                    notes_str = t.notes or ""
                    if search_query and search_query.lower() not in notes_str.lower():
                        continue
                    
                    # Match Category
                    if category_filter != "All Categories" and t.category_or_source != category_filter:
                        continue
                        
                    # Match Type
                    tx_type_display = "INCOME" if t.tx_type == "income" else "EXPENSE"
                    if type_filter != "All Types" and tx_type_display != type_filter:
                        continue
                        
                    rows.append({
                        "ID": t.id,
                        "Date": t.date_time.strftime("%Y-%m-%d"),
                        "Type": tx_type_display,
                        "Amount (₹)": float(t.amount),
                        "Category": t.category_or_source,
                        "Description / Remarks": t.notes or "—",
                    })

                if not rows:
                    st.info("No transactions match the selected filters.")
                else:
                    df = pd.DataFrame(rows)
                    limit = st.selectbox("Show how many rows?", [5, 10, 20, 50], index=1, key="passbook_limit_dropdown")
                    display_df = df.head(limit)
                    
                    st.dataframe(
                        display_df.style.format({"Amount (₹)": "{:,.2f}"}), 
                        use_container_width=True, 
                        height=280,
                        hide_index=True
                    )

                    st.markdown("<br/>", unsafe_allow_html=True)
                    sel_col1, sel_col2 = st.columns([2, 1])
                    with sel_col1:
                        visible_rows = rows[:limit]
                        sel = st.selectbox(
                            "Select a row to change or delete", 
                            options=[f"{r['ID']} | {r['Date']} | ₹{r['Amount (₹)']} ({r['Category']})" for r in visible_rows]
                        )
                    
                    with sel_col2:
                        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                        btn_c1, btn_c2 = st.columns(2)
                        sel_id = int(sel.split(" | ")[0]) if sel else None
                        if btn_c1.button("✏️ Edit Row", use_container_width=True) and sel_id:
                            st.session_state.edit_tx_id = sel_id
                        if btn_c2.button("🗑️ Delete Row", use_container_width=True) and sel_id:
                            st.session_state.delete_tx_id = sel_id

                    # Delete Confirm Dialog
                    if st.session_state.get("delete_tx_id") == sel_id:
                        st.error(f"Are you sure you want to permanently delete transaction row #{sel_id}?")
                        if st.button("Yes, Delete Permanently", type="primary", use_container_width=True):
                            repo.delete_transaction(sel_id, user.id)
                            st.toast("Row deleted from passbook logs.", icon="🗑️")
                            del st.session_state["delete_tx_id"]
                            st.rerun()

                    # Edit Record Dialog
                    if st.session_state.get("edit_tx_id") == sel_id:
                        etx = repo.get_transaction_by_id(sel_id)
                        if etx and etx.user_id == user.id:
                            st.markdown("---")
                            st.markdown(f"### Change Entry Form: ID #{sel_id}")
                            with st.form(f"edit_tx_form_{sel_id}"):
                                m_type = st.selectbox("Entry Type", ["expense", "income"], index=0 if etx.tx_type == "expense" else 1)
                                m_date = st.date_input("Date Changed", value=etx.date_time.date())
                                m_amount = st.number_input("Amount (₹)", value=etx.amount, format="%.2f")
                                m_notes = st.text_area("Add Notes / Remarks", value=etx.notes or "")
                                if st.form_submit_button("Save Changes", use_container_width=True):
                                    new_dt = datetime(m_date.year, m_date.month, m_date.day, etx.date_time.hour, etx.date_time.minute)
                                    repo.update_transaction(sel_id, user_id=user.id, tx_type=m_type, date_time=new_dt, amount=float(m_amount), notes=m_notes)
                                    st.toast("Changes saved successfully!", icon="📝")
                                    del st.session_state["edit_tx_id"]
                                    st.rerun()
        except Exception as e:
            logger.exception("Error reading passbook: %s", e)

elif page == "Add Money Entry":
    st.subheader("Log Income or Expenses")
    st.caption("Write down a single entry to add it to your monthly logs.")

    if not user:
        st.error("Login verification missing.")
    else:
        with st.form("add_tx_form"):
            form_col1, form_col2 = st.columns(2)
            with form_col1:
                tx_type = st.selectbox("Is this an Income or Expense?", ["expense", "income"])
                amount = st.number_input("Amount (in Rupees)", min_value=0.0, format="%.2f")
            with form_col2:
                date_val = st.date_input("Transaction Date", value=datetime.now(timezone.utc).date())
                currency = "INR"

            cats = repo.list_categories(user.id)
            cat_names = [c.name for c in cats] if cats else ["Other Spending"]
            category_or_source = st.selectbox("Category Group", options=cat_names)
            
            if st.checkbox("Create a custom category name text right now"):
                category_or_source = st.text_input("Type custom category name here", value="Entertainment")

            notes = st.text_area("Remarks / Notes (Shop name, item descriptions, etc.)")
            submit_tx = st.form_submit_button("Save onto Ledger", use_container_width=True)

        if submit_tx:
            if amount <= 0:
                st.error("Please enter an amount that is greater than zero.")
            else:
                dt = datetime(date_val.year, date_val.month, date_val.day, 12, 0)
                repo.upsert_category(user.id, category_or_source)
                tx = repo.add_transaction(user.id, tx_type, dt, float(amount), currency, category_or_source, notes or None)
                st.success(f"Successfully saved entry under reference number: #{tx.id}")
                st.toast("Transaction written onto Passbook!", icon="💸")

elif page == "Spending Analytics":
    st.subheader("Your Money Analytics Graphs")
    st.caption("Simple chart breakdowns showing exactly where your money goes.")

    from services.analytics import monthly_totals, category_totals_for_month, daily_breakdown
    import pandas as pd
    import plotly.express as px

    if not user:
        st.error("Login verification failed.")
    else:
        months = st.slider("Show past timeline (Months)", min_value=3, max_value=24, value=6)
        mt = monthly_totals(repo, user.id, months=months)
        
        if mt.empty:
            st.info("Not enough data to load the graph. Please log transactions first.")
        else:
            mt_long = mt.melt(id_vars=["month"], value_vars=["income", "expense"], var_name="Type", value_name="Amount (₹)")
            
            grid_color = 'rgba(255,255,255,0.06)' if st.session_state.theme == "dark" else 'rgba(0,0,0,0.06)'
            text_theme_color = "#94a3b8" if st.session_state.theme == "dark" else "#475569"
            title_theme_color = "#f8fafc" if st.session_state.theme == "dark" else "#0f172a"

            fig = px.line(
                mt_long, x="month", y="Amount (₹)", color="Type", markers=True,
                title="Timeline: Money Income vs Spending Trends",
                template="plotly_dark" if st.session_state.theme == "dark" else "plotly_white",
                color_discrete_sequence=["#10b981", "#ef4444"]
            )
            fig.update_layout(
                font_family="Plus Jakarta Sans",
                font_color=text_theme_color,
                title_font_color=title_theme_color,
                title_font_size=16,
                margin=dict(l=20, r=20, t=50, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            fig.update_xaxes(showgrid=True, gridcolor=grid_color, linecolor=grid_color)
            fig.update_yaxes(showgrid=True, gridcolor=grid_color, linecolor=grid_color)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("<br/>", unsafe_allow_html=True)
            st.subheader("Category-Wise Sharing Analysis")
            this_month = st.date_input("Pick a month to analyze", value=datetime.now(timezone.utc).date().replace(day=1))
            
            ct = category_totals_for_month(repo, user.id, this_month.year, this_month.month)
            if ct.empty:
                st.info("No logs found for this specific selected month.")
            else:
                if "expense" in ct.columns:
                    top = ct.sort_values(by="expense", ascending=False).head(10)
                    fig2 = px.bar(
                        top, x="category", y="expense", 
                        title=f"Where you spent money in {this_month.year}-{this_month.month:02d} (Top Groups)",
                        template="plotly_dark" if st.session_state.theme == "dark" else "plotly_white",
                        color_discrete_sequence=["#6366f1" if st.session_state.theme == "dark" else "#4f46e5"]
                    )
                    fig2.update_layout(
                        font_family="Plus Jakarta Sans",
                        font_color=text_theme_color,
                        title_font_color=title_theme_color,
                        title_font_size=16,
                        margin=dict(l=20, r=20, t=50, b=20),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )
                    fig2.update_xaxes(showgrid=False, linecolor=grid_color)
                    fig2.update_yaxes(showgrid=True, gridcolor=grid_color, linecolor=grid_color)
                    st.plotly_chart(fig2, use_container_width=True)

elif page == "Monthly Budgets":
    st.subheader("Set Spending Limits & Budgets")
    st.caption("Enforce monthly budget caps on your spending to control cash leakages.")

    from services.budgets import evaluate_budgets

    if not user:
        st.error("Login verification missing.")
    else:
        with st.form("set_budget_form"):
            b_month = st.text_input("Budget Target Month (Format: YYYY-MM)", value=datetime.now(timezone.utc).strftime("%Y-%m"))
            cats = repo.list_categories(user.id)
            cat_options = ["(Total Monthly Budget Cap)"] + [c.name for c in cats]
            sel = st.selectbox("Which spending group limit?", options=cat_options)
            amt = st.number_input("Maximum Budget Spending Cap (₹)", min_value=0.0, format="%.2f")
            submit_budget = st.form_submit_button("Apply Budget Ceiling", use_container_width=True)

        if submit_budget:
            cat_id = next((c.id for c in cats if c.name == sel), None) if sel != "(Total Monthly Budget Cap)" else None
            repo.set_budget(user.id, b_month, amt, category_id=cat_id)
            st.success("Budget limit applied successfully!")
            st.toast("Budget configuration saved!", icon="🛡️")
            st.rerun()

        st.markdown("---")
        st.subheader("Budget Safety Status Checks")
        evals = evaluate_budgets(repo, user.id)
        if not evals:
            st.info("You haven't added any budget limit parameters for this active month cycle.")
        else:
            cols = st.columns(min(len(evals), 3))
            for i, b in enumerate(evals):
                c = cols[i % len(cols)]
                label = "Global Budget Cap" if b["category_id"] is None else f"Category Group"
                status_color = "#10B981" if b["status"] == "green" else ("#F59E0B" if b["status"] == "orange" else "#EF4444")
                
                c.markdown(f"""
                    <div class="finance-card" style="border-left: 5px solid {status_color}; color: {text_color} !important;">
                        <div class="card-label">{label} Safety Level</div>
                        <div style="font-size: 14px; margin: 4px 0; color: {text_color} !important;">Max Allowed Cap: <b style="color: {text_color} !important;">₹{b['limit']:.2f}</b></div>
                        <div style="font-size: 14px; margin-bottom: 12px; color: {text_color} !important;">Actually Spent: <b style="color: {text_color} !important;">₹{b['spent']:.2f}</b></div>
                    </div>
                """, unsafe_allow_html=True)
                c.progress(min(int(b["ratio"] * 100), 100))

elif page == "Future Forecast":
    st.subheader("Next Month Category-Wise Spending Estimator")
    st.caption("A data projection tool that looks at previous spending cycles to forecast next month's category expenses.")

    from services.forecast import forecast_categories_next_month, forecast_next_month
    from services.analytics import category_totals_for_month
    import pandas as pd
    import plotly.express as px

    if not user:
        st.error("Login session context missing.")
    else:
        lookback = st.slider("Lookback Memory window depth (Months)", 1, 12, 3, key="forecast_lookback_slider")
        
        # Calculate individual category projections
        forecasts = forecast_categories_next_month(repo, user.id, lookback_months=lookback)
        
        if not forecasts:
            st.info("Estimation engine needs at least 2 or more months of logged data to run category-level forecasts.")
        else:
            # Let's get current month category expenses for comparison
            now = datetime.now()
            current_ct = category_totals_for_month(repo, user.id, now.year, now.month)
            
            current_cat_map = {}
            if not current_ct.empty and "expense" in current_ct.columns:
                current_cat_map = dict(zip(current_ct["category"], current_ct["expense"]))
                
            comparison_rows = []
            all_cats = sorted(list(set(list(forecasts.keys()) + list(current_cat_map.keys()))))
            
            for cat in all_cats:
                curr_val = current_cat_map.get(cat, 0.0)
                pred_val = forecasts.get(cat, 0.0)
                # Only include categories with non-zero values
                if curr_val > 0.0 or pred_val > 0.0:
                    comparison_rows.append({
                        "Category": cat,
                        "Current Month (₹)": curr_val,
                        "Predicted Next Month (₹)": pred_val
                    })
                    
            if comparison_rows:
                comp_df = pd.DataFrame(comparison_rows)
                
                # Plotly side-by-side grouped bar chart
                comp_long = comp_df.melt(
                    id_vars=["Category"], 
                    value_vars=["Current Month (₹)", "Predicted Next Month (₹)"], 
                    var_name="Period", 
                    value_name="Amount (₹)"
                )
                
                grid_color = 'rgba(255,255,255,0.06)' if st.session_state.theme == "dark" else 'rgba(0,0,0,0.06)'
                text_theme_color = "#94a3b8" if st.session_state.theme == "dark" else "#475569"
                title_theme_color = "#f8fafc" if st.session_state.theme == "dark" else "#0f172a"
                
                fig = px.bar(
                    comp_long, 
                    x="Category", 
                    y="Amount (₹)", 
                    color="Period", 
                    barmode="group",
                    title="Predicted vs Current Month Category Spending",
                    template="plotly_dark" if st.session_state.theme == "dark" else "plotly_white",
                    color_discrete_sequence=["#94a3b8", "#6366f1"] if st.session_state.theme == "dark" else ["#94a3b8", "#4f46e5"]
                )
                
                fig.update_layout(
                    font_family="Plus Jakarta Sans",
                    font_color=text_theme_color,
                    title_font_color=title_theme_color,
                    title_font_size=16,
                    margin=dict(l=20, r=20, t=50, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                fig.update_yaxes(showgrid=True, gridcolor=grid_color, linecolor=grid_color)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Table Breakdown
                st.markdown("<br/>", unsafe_allow_html=True)
                st.subheader("Category Forecast Ledger")
                st.dataframe(
                    comp_df.style.format({
                        "Current Month (₹)": "{:,.2f}",
                        "Predicted Next Month (₹)": "{:,.2f}"
                    }),
                    use_container_width=True,
                    hide_index=True
                )
                
            # Estimated total
            total_pred = sum(forecasts.values())
            st.markdown(f"""
                <div class="finance-card" style="max-width: 500px; border-top: 4px solid #3B82F6; margin-top: 20px;">
                    <div class="card-label">Estimated Total Expense Next Month</div>
                    <div class="card-value" style="color: #3B82F6;">₹{total_pred:,.2f}</div>
                    <div class="card-footer">Aggregation of individual category projections over a rolling lookback window.</div>
                </div>
            """, unsafe_allow_html=True)

elif page == "Manage Categories":
    st.subheader("Customize Category Groups")
    st.caption("Add, rename, or drop custom categories used in your log book records.")

    if not user:
        st.error("Login validation error.")
    else:
        st.subheader("Active Groups Category List")
        try:
            categories = repo.list_categories(user.id)
            if categories:
                for c in categories:
                    st.markdown(f"📦 `Code: {c.id:02d}` **{c.name}**")
            else:
                st.info("No custom categories loaded yet.")
        except Exception as e:
            st.error("Failed to load category trees.")

        st.markdown("---")
        add_col, ren_col, del_col = st.columns(3)
        
        with add_col:
            st.markdown("**Add a Category**")
            new_cat = st.text_input("New Category Name", key="new_cat")
            if st.button("Create Category Group", use_container_width=True):
                if new_cat:
                    repo.upsert_category(user.id, new_cat)
                    st.toast("New category saved!")
                    st.rerun()
                else:
                    st.error("Name field cannot be left empty.")
                    
        with ren_col:
            st.markdown("**Rename Category**")
            cat_map = {c.name: c.id for c in categories} if categories else {}
            if cat_map:
                sel = st.selectbox("Choose Category to change", options=list(cat_map.keys()))
                rename_to = st.text_input("Type new replacement name", key="ren_to")
                if st.button("Apply New Name", use_container_width=True):
                    if rename_to:
                        repo.update_category_name(cat_map[sel], rename_to)
                        st.toast("Category renamed successfully.")
                        st.rerun()
            else:
                st.caption("No categories available to rename.")
                
        with del_col:
            st.markdown("**Delete Category**")
            if cat_map:
                dsel = st.selectbox("Choose Category to remove", options=list(cat_map.keys()), key="del_sel")
                if st.button("Remove Category Group", use_container_width=True, type="primary"):
                    repo.delete_category(cat_map[dsel], user.id)
                    st.toast("Category removed successfully.", icon="💥")
                    st.rerun()
            else:
                st.caption("No categories available to delete.")