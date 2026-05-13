import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
from streamlit_oauth import OAuth2Component

load_dotenv()
# ── page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GOOGLE OAUTH CONFIG ─────────────────────

CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"

TOKEN_URL = "https://oauth2.googleapis.com/token"

REDIRECT_URI ="https://likhithadevarasetty-sourcesys-task-applicationapp-dhqseu.streamlit.app/component/streamlit_oauth.authorize_button/"


# ── global styles ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        /* main background */
        .stApp { background: #0f1117; }

        /* sidebar */
        section[data-testid="stSidebar"] {
            background: #1a1d27;
            border-right: 1px solid #2e3149;
        }

        /* metric cards */
        div[data-testid="metric-container"] {
            background: #1e2130;
            border: 1px solid #2e3149;
            border-radius: 12px;
            padding: 18px 22px;
        }

        /* headings */
        h1, h2, h3 { color: #e2e8f0 !important; }

        /* login card */
        .login-card {
            max-width: 420px;
            margin: 80px auto 0 auto;
            background: #1e2130;
            border: 1px solid #2e3149;
            border-radius: 16px;
            padding: 48px 40px 40px 40px;
        }

        .login-title {
            text-align: center;
            font-size: 26px;
            font-weight: 700;
            color: #e2e8f0;
            margin-bottom: 6px;
        }

        .login-sub {
            text-align: center;
            color: #8892a4;
            font-size: 14px;
            margin-bottom: 32px;
        }

        /* section divider label */
        .section-label {
            font-size: 11px;
            letter-spacing: 1.4px;
            text-transform: uppercase;
            color: #6b7280;
            margin: 28px 0 10px 0;
        }

        /* pill badge */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-green  { background: #14532d; color: #4ade80; }
        .badge-yellow { background: #713f12; color: #fbbf24; }
        .badge-red    { background: #7f1d1d; color: #f87171; }
    </style>
    """,
    unsafe_allow_html=True,
)



# ── session state bootstrap ────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
def login_page():
    st.markdown(
        """
        <div class="login-card">
            <div class="login-title">🎓 Student Analytics</div>
            <div class="login-sub">Sign in to access the dashboard</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)

    # OAuth component
    oauth2 = OAuth2Component(
        CLIENT_ID,
        CLIENT_SECRET,
        AUTHORIZE_URL,
        TOKEN_URL,
        TOKEN_URL,
    )

    _, col, _ = st.columns([1, 1.5, 1])

    with col:

        result = oauth2.authorize_button(
            name=" Continue with Google",
            icon="https://www.google.com/favicon.ico",
            redirect_uri=REDIRECT_URI,
            scope="openid email profile",
            key="google",
            use_container_width=True,
        )

        # after successful login
        if result and "token" in result:

            user_info = result["token"]

            st.session_state.logged_in = True
            st.session_state.username = "Google User"

            st.success("Login successful!")
            st.rerun()
            
        st.markdown(
            "<div style='margin-top:20px; text-align:center; color:#6b7280; font-size:12px;'>"
           
            "</div>",
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
#  DATA LOADER
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv("student_data.csv")
    df.columns = df.columns.str.strip()
    df["NAME"] = df["NAME"].str.title()
    df["TUTION"] = df["TUTION"].str.lower()
    df["HEALTH"] = df["HEALTH"].str.lower()
    df["STRESS"] = df["STRESS"].str.lower()
    df["DAILY WORK"] = df["DAILY WORK"].str.title()
    return df


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD PAGE
# ══════════════════════════════════════════════════════════════════════════════
def dashboard_page():
    df = load_data()

    # ── sidebar ────────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(
            f"<div style='color:#a5b4fc; font-weight:700; font-size:18px; "
            f"margin-bottom:4px;'>🎓 Student Analytics</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='color:#6b7280; font-size:13px; margin-bottom:20px;'>"
            f"Logged in as <b style='color:#e2e8f0;'>{st.session_state.username}</b></div>",
            unsafe_allow_html=True,
        )
        st.divider()

        st.markdown("<div class='section-label'>Filters</div>", unsafe_allow_html=True)

        # age filter
        min_age, max_age = int(df["AGE"].min()), int(df["AGE"].max())
        age_range = st.slider("Age range", min_age, max_age, (min_age, max_age))

        # stress filter
        stress_opts = ["All"] + sorted(df["STRESS"].unique().tolist())
        stress_pick = st.selectbox("Stress level", stress_opts)

        # health filter
        health_opts = ["All"] + sorted(df["HEALTH"].unique().tolist())
        health_pick = st.selectbox("Health status", health_opts)

        # tution filter
        tution_opts = ["All", "yes", "no"]
        tution_pick = st.selectbox("Has tuition?", tution_opts)

        # daily work filter
        dw_opts = ["All"] + sorted(df["DAILY WORK"].unique().tolist())
        dw_pick = st.selectbox("Daily work performance", dw_opts)

        st.divider()
        if st.button("🚪 Logout", width='stretch'):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    # ── apply filters ──────────────────────────────────────────────────────────
    filtered = df[df["AGE"].between(age_range[0], age_range[1])]
    if stress_pick  != "All": filtered = filtered[filtered["STRESS"]     == stress_pick]
    if health_pick  != "All": filtered = filtered[filtered["HEALTH"]     == health_pick]
    if tution_pick  != "All": filtered = filtered[filtered["TUTION"]     == tution_pick]
    if dw_pick      != "All": filtered = filtered[filtered["DAILY WORK"] == dw_pick]

    # ── page header ────────────────────────────────────────────────────────────
    st.markdown("## 📊 Student Performance Dashboard")
    st.markdown(
        f"<div style='color:#6b7280; margin-bottom:24px;'>"
        f"Showing <b style='color:#a5b4fc;'>{len(filtered)}</b> of "
        f"<b style='color:#a5b4fc;'>{len(df)}</b> students</div>",
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info("No students match the selected filters. Try adjusting them.")
        return

    # ── KPI row ────────────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Students",   len(filtered))
    k2.metric("Avg Exam Score",   f"{filtered['EXAM SCORE'].mean():.1f}")
    k3.metric("Avg Attendance",   f"{filtered['ATTENDANCE'].mean():.1f}%")
    k4.metric("Avg Self Study",   f"{filtered['SELF STUDY'].mean():.1f} hrs")
    k5.metric("Avg Video Games",  f"{filtered['VIDEO GAMES'].mean():.1f} hrs")

    st.write("")

    # ── tab layout ─────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Performance", "📋 Student Records", "🔍 Correlation", "📌 Summary Stats"]
    )

    # ─── TAB 1 : Performance ──────────────────────────────────────────────────
    with tab1:
        col_a, col_b = st.columns(2)

        with col_a:
            # exam score distribution
            fig = px.histogram(
                filtered, x="EXAM SCORE", nbins=12,
                title="Exam Score Distribution",
                color_discrete_sequence=["#818cf8"],
                template="plotly_dark",
            )
            fig.update_layout(
                paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
                font_color="#e2e8f0", showlegend=False,
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig, width='stretch')

        with col_b:
            # attendance vs exam score scatter
            fig = px.scatter(
                filtered, x="ATTENDANCE", y="EXAM SCORE",
                color="STRESS", size="SELF STUDY",
                hover_data=["NAME"],
                title="Attendance vs Exam Score (size = self-study)",
                color_discrete_map={"low": "#4ade80", "moderate": "#fbbf24", "high": "#f87171"},
                template="plotly_dark",
            )
            fig.update_layout(
                paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
                font_color="#e2e8f0",
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig, width='stretch')

        col_c, col_d = st.columns(2)

        with col_c:
            # stress level pie
            stress_counts = filtered["STRESS"].value_counts().reset_index()
            stress_counts.columns = ["Stress Level", "Count"]
            fig = px.pie(
                stress_counts, names="Stress Level", values="Count",
                title="Stress Level Breakdown",
                color="Stress Level",
                color_discrete_map={"low": "#4ade80", "moderate": "#fbbf24", "high": "#f87171"},
                template="plotly_dark",
                hole=0.4,
            )
            fig.update_layout(
                paper_bgcolor="#1e2130", font_color="#e2e8f0",
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig, width='stretch')

        with col_d:
            # daily work performance bar
            dw_avg = (
                filtered.groupby("DAILY WORK")["EXAM SCORE"]
                .mean()
                .reset_index()
                .sort_values("EXAM SCORE", ascending=False)
            )
            fig = px.bar(
                dw_avg, x="DAILY WORK", y="EXAM SCORE",
                title="Avg Exam Score by Daily Work Performance",
                color="DAILY WORK",
                color_discrete_map={
                    "Satisfactory": "#4ade80",
                    "Below Average": "#fbbf24",
                    "Poor": "#f87171",
                },
                template="plotly_dark",
            )
            fig.update_layout(
                paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
                font_color="#e2e8f0", showlegend=False,
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig, width='stretch')

        # video games vs exam score
        fig = px.box(
            filtered, x="VIDEO GAMES", y="EXAM SCORE",
            title="Video Game Hours vs Exam Score",
            color_discrete_sequence=["#818cf8"],
            template="plotly_dark",
        )
        fig.update_layout(
            paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
            font_color="#e2e8f0",
            margin=dict(l=10, r=10, t=40, b=10),
        )
        st.plotly_chart(fig, width='stretch')

    # ─── TAB 2 : Student Records ──────────────────────────────────────────────
    with tab2:
        st.markdown("### Individual Student Records")

        search = st.text_input("🔎 Search by student name", placeholder="Type a name…")
        if search:
            records = filtered[filtered["NAME"].str.lower().str.contains(search.lower())]
        else:
            records = filtered

        def score_badge(score):
            if score >= 85:
                return f"<span class='badge badge-green'>{score}</span>"
            elif score >= 65:
                return f"<span class='badge badge-yellow'>{score}</span>"
            else:
                return f"<span class='badge badge-red'>{score}</span>"

        # build display table
        display = records.copy()
        display = display.reset_index(drop=True)
        display.index = display.index + 1

        st.dataframe(
            display,
            width='stretch',
            height=420,
        )

        st.markdown(
            "<div style='color:#6b7280; font-size:12px; margin-top:8px;'>"
            "🟢 85+ &nbsp; 🟡 65–84 &nbsp; 🔴 Below 65</div>",
            unsafe_allow_html=True,
        )

        # download button
        csv_data = records.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download filtered data as CSV",
            data=csv_data,
            file_name="filtered_students.csv",
            mime="text/csv",
        )

    # ─── TAB 3 : Correlation ──────────────────────────────────────────────────
    with tab3:
        st.markdown("### Variable Relationships")

        numeric_cols = ["AGE", "ATTENDANCE", "EXAM SCORE", "VIDEO GAMES", "SELF STUDY"]
        x_axis = st.selectbox("X axis", numeric_cols, index=1)
        y_axis = st.selectbox("Y axis", numeric_cols, index=2)

        color_by = st.selectbox(
            "Color by",
            ["STRESS", "HEALTH", "TUTION", "DAILY WORK"],
        )

        color_maps = {
            "STRESS":     {"low": "#4ade80", "moderate": "#fbbf24", "high": "#f87171"},
            "HEALTH":     {"good": "#4ade80", "bad": "#f87171"},
            "TUTION":     {"yes": "#60a5fa", "no": "#f87171"},
            "DAILY WORK": {
                "Satisfactory": "#4ade80",
                "Below Average": "#fbbf24",
                "Poor": "#f87171",
            },
        }

        fig = px.scatter(
            filtered, x=x_axis, y=y_axis,
            color=color_by,
            hover_data=["NAME"],
            trendline="ols",
            color_discrete_map=color_maps.get(color_by, {}),
            template="plotly_dark",
            title=f"{x_axis} vs {y_axis} — coloured by {color_by}",
        )
        fig.update_layout(
            paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
            font_color="#e2e8f0",
            margin=dict(l=10, r=10, t=50, b=10),
        )
        st.plotly_chart(fig, width='stretch')

        # correlation heatmap
        st.markdown("#### Numeric Correlation Heatmap")
        corr = filtered[numeric_cols].corr()
        fig2 = go.Figure(
            data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.index,
                colorscale="RdBu",
                zmid=0,
                text=[[f"{v:.2f}" for v in row] for row in corr.values],
                texttemplate="%{text}",
            )
        )
        fig2.update_layout(
            paper_bgcolor="#1e2130", plot_bgcolor="#1e2130",
            font_color="#e2e8f0",
            margin=dict(l=10, r=10, t=20, b=10),
            height=400,
        )
        st.plotly_chart(fig2, width='stretch')

    # ─── TAB 4 : Summary Stats ────────────────────────────────────────────────
    with tab4:
        st.markdown("### Summary Statistics")

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("#### Numeric columns")
            st.dataframe(
                filtered[["AGE","ATTENDANCE","EXAM SCORE","VIDEO GAMES","SELF STUDY"]]
                .describe()
                .round(2),
                width='stretch',
            )

        with col_right:
            st.markdown("#### Categorical breakdowns")

            for cat in ["STRESS", "HEALTH", "TUTION", "DAILY WORK"]:
                counts = filtered[cat].value_counts().reset_index()
                counts.columns = [cat, "Count"]
                counts["% Share"] = (counts["Count"] / counts["Count"].sum() * 100).round(1)
                st.dataframe(counts, width='stretch', hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.logged_in:
    dashboard_page()
else:
    login_page()