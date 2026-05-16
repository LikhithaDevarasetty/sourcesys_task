import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
from pathlib import Path

# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SalesVision Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── helpers ───────────────────────────────────────────────────────────────────
# BASE_DIR resolves to the folder where dashboard.py lives, so file
# lookups work correctly both locally and on Streamlit Cloud.
BASE_DIR = Path(__file__).parent.resolve()

def img_to_b64(filename):
    return base64.b64encode((BASE_DIR / filename).read_bytes()).decode()

BG   = img_to_b64("bg.png")
LOGO = img_to_b64("logo.png")

# ── global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ---------- base ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background-image: url("data:image/png;base64,{BG}");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}}

/* dark overlay so text is readable */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(5, 8, 30, 0.72);
    z-index: 0;
    pointer-events: none;
}}

section[data-testid="stSidebar"] > div:first-child {{
    background: rgba(10, 14, 50, 0.92);
    border-right: 1px solid rgba(100, 120, 255, 0.25);
    backdrop-filter: blur(18px);
}}

/* ---------- sidebar controls ---------- */
.stSelectbox label,
.stMultiSelect label,
.stRadio label {{
    color: #a0b4ff !important;
    font-weight: 500;
    font-size: 0.82rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}}

div[data-baseweb="select"] > div {{
    background: rgba(30, 40, 100, 0.7) !important;
    border: 1px solid rgba(100, 130, 255, 0.4) !important;
    border-radius: 10px !important;
    color: #e0e8ff !important;
}}

div[data-baseweb="select"] > div:focus-within {{
    border-color: #6c7fff !important;
    box-shadow: 0 0 0 2px rgba(108, 127, 255, 0.35) !important;
}}

/* ---------- metric cards ---------- */
.metric-card {{
    background: linear-gradient(135deg, rgba(20,28,90,0.85), rgba(40,20,100,0.75));
    border: 1px solid rgba(130, 100, 255, 0.35);
    border-radius: 16px;
    padding: 22px 24px;
    backdrop-filter: blur(14px);
    transition: transform 0.2s, box-shadow 0.2s;
    text-align: center;
}}

.metric-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(100, 80, 255, 0.3);
}}

.metric-label {{
    color: #8899dd;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 6px;
}}

.metric-value {{
    color: #ffffff;
    font-size: 1.9rem;
    font-weight: 700;
    line-height: 1.1;
}}

.metric-delta {{
    font-size: 0.78rem;
    margin-top: 5px;
    color: #66ffb2;
}}

/* ---------- chart wrapper ---------- */
.chart-box {{
    background: rgba(10, 15, 55, 0.75);
    border: 1px solid rgba(90, 110, 255, 0.25);
    border-radius: 18px;
    padding: 20px;
    backdrop-filter: blur(16px);
    margin-bottom: 20px;
}}

.chart-title {{
    color: #c0caff;
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(100, 120, 255, 0.2);
}}

/* ---------- section headings ---------- */
h1, h2, h3 {{
    color: #dce6ff !important;
}}

/* ---------- logo bar ---------- */
.logo-bar {{
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 10px 0 18px;
}}

.logo-bar img {{
    width: 90px;
    border-radius: 12px;
}}

.logo-bar-text {{
    font-size: 1.05rem;
    font-weight: 700;
    color: #a8baff;
    letter-spacing: 0.06em;
    line-height: 1.35;
}}

/* ---------- sidebar section divider ---------- */
.sidebar-divider {{
    border: none;
    border-top: 1px solid rgba(100, 130, 255, 0.2);
    margin: 14px 0;
}}

/* ---------- streamlit element tweaks ---------- */
div[data-testid="stHorizontalBlock"] {{
    gap: 16px;
}}

.stPlotlyChart {{
    border-radius: 14px;
    overflow: hidden;
}}

footer {{visibility: hidden;}}
#MainMenu {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# ── load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(BASE_DIR / "train.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  dayfirst=True)
    df["Year"]       = df["Order Date"].dt.year
    df["Month"]      = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.strftime("%b")
    df["Quarter"]    = df["Order Date"].dt.to_period("Q").astype(str)
    return df

df = load_data()

# ── plotly theme ──────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#c0caff", size=12),
    legend=dict(
        bgcolor="rgba(15,20,70,0.6)",
        bordercolor="rgba(100,130,255,0.3)",
        borderwidth=1,
        font=dict(color="#c0caff"),
    ),
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(
        gridcolor="rgba(100,130,255,0.12)",
        zerolinecolor="rgba(100,130,255,0.2)",
        tickfont=dict(color="#8899cc"),
    ),
    yaxis=dict(
        gridcolor="rgba(100,130,255,0.12)",
        zerolinecolor="rgba(100,130,255,0.2)",
        tickfont=dict(color="#8899cc"),
    ),
)

PALETTE = px.colors.sequential.Plasma

# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="logo-bar">
        <img src="data:image/png;base64,{LOGO}" />
        <div class="logo-bar-text">SalesVision<br>Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown("### 🎛️ Filters")

    all_years = sorted(df["Year"].unique())
    sel_years = st.multiselect("Select Year(s)", all_years, default=all_years)

    all_regions = sorted(df["Region"].unique())
    sel_regions = st.multiselect("Select Region(s)", all_regions, default=all_regions)

    all_segs = sorted(df["Segment"].unique())
    sel_segs = st.multiselect("Select Segment(s)", all_segs, default=all_segs)

    all_cats = sorted(df["Category"].unique())
    sel_cats = st.multiselect("Select Category(s)", all_cats, default=all_cats)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown("### 📐 Chart Axes")

    x_options = ["Month Name", "Quarter", "Category", "Sub-Category", "Region", "Segment", "Ship Mode", "State"]
    y_options = ["Sales"]
    color_options = ["Category", "Segment", "Region", "Ship Mode", "Year"]

    x_axis    = st.selectbox("X-Axis",    x_options,    index=0)
    color_by  = st.selectbox("Color By",  color_options, index=0)
    chart_type = st.radio("Chart Type", ["Bar", "Line", "Area", "Scatter", "Pie"], index=0)

# ── filter data ───────────────────────────────────────────────────────────────
mask = (
    df["Year"].isin(sel_years) &
    df["Region"].isin(sel_regions) &
    df["Segment"].isin(sel_segs) &
    df["Category"].isin(sel_cats)
)
fdf = df[mask].copy()

if fdf.empty:
    st.warning("No data matches the selected filters. Please adjust.")
    st.stop()

# ── top logo bar ──────────────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.image(str(BASE_DIR / "logo.png"), width=80)
with col_title:
    st.markdown("""
    <h1 style='margin:0; padding-top:10px; font-size:2rem; letter-spacing:0.05em;'>
        SalesVision Dashboard
    </h1>
    <p style='color:#7088cc; margin:0; font-size:0.85rem;'>
        Sales Intelligence · Built with Streamlit & Plotly
    </p>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── KPI cards ─────────────────────────────────────────────────────────────────
total_sales  = fdf["Sales"].sum()
total_orders = fdf["Order ID"].nunique()
avg_order    = fdf.groupby("Order ID")["Sales"].sum().mean()
top_cat      = fdf.groupby("Category")["Sales"].sum().idxmax()

k1, k2, k3, k4 = st.columns(4)

for col, label, value, delta in [
    (k1, "Total Sales",    f"${total_sales:,.0f}",    "↑ All selected periods"),
    (k2, "Total Orders",   f"{total_orders:,}",       "Unique order IDs"),
    (k3, "Avg Order Value",f"${avg_order:,.0f}",      "Per order"),
    (k4, "Top Category",   top_cat,                   "By total revenue"),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── helper: wrap chart in styled box ─────────────────────────────────────────
def chart_box(title, fig):
    st.markdown(f'<div class="chart-box"><div class="chart-title">{title}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── main dynamic chart ────────────────────────────────────────────────────────
agg = fdf.groupby([x_axis, color_by], as_index=False)["Sales"].sum()
agg = agg.sort_values(x_axis)

title_main = f"Sales by {x_axis} · Colored by {color_by}"

if chart_type == "Bar":
    fig_main = px.bar(agg, x=x_axis, y="Sales", color=color_by,
                      barmode="group", color_discrete_sequence=PALETTE)
elif chart_type == "Line":
    fig_main = px.line(agg, x=x_axis, y="Sales", color=color_by,
                       markers=True, color_discrete_sequence=PALETTE)
elif chart_type == "Area":
    fig_main = px.area(agg, x=x_axis, y="Sales", color=color_by,
                       color_discrete_sequence=PALETTE)
elif chart_type == "Scatter":
    fig_main = px.scatter(agg, x=x_axis, y="Sales", color=color_by,
                          size="Sales", color_discrete_sequence=PALETTE)
else:  # Pie
    pie_agg = fdf.groupby(x_axis, as_index=False)["Sales"].sum()
    fig_main = px.pie(pie_agg, names=x_axis, values="Sales",
                      color_discrete_sequence=PALETTE, hole=0.4)

fig_main.update_layout(**PLOTLY_LAYOUT)
chart_box(title_main, fig_main)

# ── row 2: monthly trend + region breakdown ───────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    monthly = fdf.groupby(["Year", "Month", "Month Name"], as_index=False)["Sales"].sum()
    monthly = monthly.sort_values(["Year", "Month"])
    monthly["YearStr"] = monthly["Year"].astype(str)
    fig_line = px.line(monthly, x="Month Name", y="Sales", color="YearStr",
                       markers=True, color_discrete_sequence=PALETTE,
                       category_orders={"Month Name": ["Jan","Feb","Mar","Apr","May",
                                                        "Jun","Jul","Aug","Sep","Oct","Nov","Dec"]})
    fig_line.update_layout(**PLOTLY_LAYOUT)
    chart_box("📈 Monthly Sales Trend by Year", fig_line)

with c2:
    reg = fdf.groupby("Region", as_index=False)["Sales"].sum()
    fig_reg = px.bar(reg, x="Region", y="Sales", color="Region",
                     color_discrete_sequence=PALETTE)
    fig_reg.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    chart_box("🌍 Sales by Region", fig_reg)

# ── row 3: category donut + sub-category bar ──────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    cat_df = fdf.groupby("Category", as_index=False)["Sales"].sum()
    fig_pie = px.pie(cat_df, names="Category", values="Sales",
                     color_discrete_sequence=PALETTE, hole=0.5)
    fig_pie.update_traces(textfont_color="#ffffff")
    fig_pie.update_layout(**PLOTLY_LAYOUT)
    chart_box("🗂️ Sales Share by Category", fig_pie)

with c4:
    sub = fdf.groupby("Sub-Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=True)
    fig_sub = px.bar(sub, x="Sales", y="Sub-Category", orientation="h",
                     color="Sales", color_continuous_scale="Plasma")
    fig_sub.update_layout(**PLOTLY_LAYOUT)
    fig_sub.update_layout(coloraxis_showscale=False)
    chart_box("📦 Sales by Sub-Category", fig_sub)

# ── row 4: segment funnel + ship mode ─────────────────────────────────────────
c5, c6 = st.columns(2)

with c5:
    seg_df = fdf.groupby(["Segment","Category"], as_index=False)["Sales"].sum()
    fig_seg = px.bar(seg_df, x="Segment", y="Sales", color="Category",
                     barmode="stack", color_discrete_sequence=PALETTE)
    fig_seg.update_layout(**PLOTLY_LAYOUT)
    chart_box("👥 Sales by Segment & Category", fig_seg)

with c6:
    ship_df = fdf.groupby("Ship Mode", as_index=False)["Sales"].sum()
    fig_ship = px.pie(ship_df, names="Ship Mode", values="Sales",
                      color_discrete_sequence=PALETTE, hole=0.4)
    fig_ship.update_traces(textfont_color="#ffffff")
    fig_ship.update_layout(**PLOTLY_LAYOUT)
    chart_box("🚚 Sales by Ship Mode", fig_ship)

# ── row 5: quarterly trend heatmap ────────────────────────────────────────────
q_df = fdf.groupby(["Year", "Quarter"], as_index=False)["Sales"].sum()
q_pivot = q_df.pivot(index="Year", columns="Quarter", values="Sales").fillna(0)

fig_heat = go.Figure(go.Heatmap(
    z=q_pivot.values,
    x=q_pivot.columns.tolist(),
    y=[str(y) for y in q_pivot.index.tolist()],
    colorscale="Plasma",
    hoverongaps=False,
    hovertemplate="Quarter: %{x}<br>Year: %{y}<br>Sales: $%{z:,.0f}<extra></extra>",
))
fig_heat.update_layout(**PLOTLY_LAYOUT, title="")
chart_box("🔥 Quarterly Sales Heatmap", fig_heat)

# ── top 10 states ─────────────────────────────────────────────────────────────
top_states = fdf.groupby("State", as_index=False)["Sales"].sum().nlargest(10, "Sales")
fig_state = px.bar(top_states, x="State", y="Sales", color="Sales",
                   color_continuous_scale="Plasma")
fig_state.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False)
chart_box("🏙️ Top 10 States by Sales", fig_state)

# ── footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; color:#3a4a88; font-size:0.75rem; margin-top:40px; padding-top:20px;
            border-top:1px solid rgba(80,100,255,0.15);'>
    SalesVision Dashboard · Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)