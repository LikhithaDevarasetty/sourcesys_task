import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

st.set_page_config(page_title="Data Graph Dashboard", layout="wide")

st.title("📊 Data Visualization Dashboard")
st.markdown("Upload your Excel or CSV file and explore your data with different chart types.")

# ── file upload ───────────────────────────────────────────────────────────────
uploaded_file = st.sidebar.file_uploader(
    "Upload your dataset",
    type=["xlsx", "xls", "csv"],
    help="Supports .xlsx, .xls, and .csv files"
)

if uploaded_file is None:
    st.info("👈 Please upload a file from the sidebar to get started.")
    st.stop()

# ── load data ─────────────────────────────────────────────────────────────────
# sheet selection must happen outside @st.cache_data (it calls st.selectbox)
if uploaded_file.name.lower().endswith(".csv"):
    df = pd.read_csv(uploaded_file)
else:
    xl = pd.ExcelFile(uploaded_file)
    if len(xl.sheet_names) > 1:
        chosen_sheet = st.sidebar.selectbox("Select sheet", xl.sheet_names)
    else:
        chosen_sheet = xl.sheet_names[0]
    df = pd.read_excel(xl, sheet_name=chosen_sheet)

# drop fully-empty columns to avoid junk options
df = df.dropna(axis=1, how="all")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Rows:** {len(df)}   **Columns:** {len(df.columns)}")

# ── classify columns ──────────────────────────────────────────────────────────
num_cols  = df.select_dtypes(include="number").columns.tolist()
cat_cols  = df.select_dtypes(include=["object", "category"]).columns.tolist()
date_cols = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()

# auto-detect text columns that look like dates
for c in list(cat_cols):
    try:
        parsed = pd.to_datetime(df[c], infer_datetime_format=True, errors="coerce")
        if parsed.notna().sum() > len(df) * 0.8:
            df[c] = parsed
            date_cols.append(c)
            cat_cols.remove(c)
    except Exception:
        pass

# ── helpers ───────────────────────────────────────────────────────────────────
def need(cols, label):
    if not cols:
        st.warning(f"⚠️ No **{label}** columns found in your dataset for this chart type.")
        st.stop()

def exclude(pool, *used):
    blocked = set(used)
    return [c for c in pool if c not in blocked]

def low_card(cols, max_unique=50):
    """Only columns with few unique values make sense as color / group-by."""
    return [c for c in cols if df[c].nunique() <= max_unique]

# ── chart type picker ─────────────────────────────────────────────────────────
chart_type = st.sidebar.selectbox(
    "Chart type",
    [
        "Bar Chart",
        "Line Chart",
        "Scatter Plot",
        "Pie / Donut Chart",
        "Histogram",
        "Box Plot",
        "Area Chart",
        "Heatmap (Correlation)",
    ]
)

# ── data preview ─────────────────────────────────────────────────────────────
with st.expander("🔍 Preview data", expanded=False):
    st.dataframe(df.head(50), use_container_width=True)

st.markdown("---")
st.subheader(f"📈 {chart_type}")

# ══════════════════════════════════════════════════════════════════════════════
# BAR CHART
# ══════════════════════════════════════════════════════════════════════════════
if chart_type == "Bar Chart":
    need(num_cols, "numeric")

    x_options = cat_cols + date_cols + num_cols
    need(x_options, "any")
    x_col = st.selectbox("X axis (category / date)", x_options)

    # Y must be numeric and must differ from X
    y_options = exclude(num_cols, x_col)
    if not y_options:
        st.warning("⚠️ The column you chose for X is the only numeric column. "
                   "Please pick a categorical or date column for X instead.")
        st.stop()
    y_col = st.selectbox("Y axis (numeric — will be summed per X value)", y_options)

    # Color: low-cardinality categoricals only, excluding X and Y
    color_options = low_card(exclude(cat_cols, x_col, y_col))
    color = st.selectbox(
        "Color by (optional)",
        ["None"] + color_options,
        help="Only categorical columns with ≤50 unique values are listed. "
             "High-cardinality columns like IDs are hidden to prevent errors."
    )

    orient = st.radio("Orientation", ["Vertical", "Horizontal"], horizontal=True)

    if color == "None":
        agg_df = df.groupby(x_col, as_index=False)[y_col].sum()
        if orient == "Vertical":
            fig = px.bar(agg_df, x=x_col, y=y_col, text_auto=True)
        else:
            fig = px.bar(agg_df, x=y_col, y=x_col, orientation="h", text_auto=True)
    else:
        agg_df = df.groupby([x_col, color], as_index=False)[y_col].sum()
        if orient == "Vertical":
            fig = px.bar(agg_df, x=x_col, y=y_col, color=color, text_auto=True)
        else:
            fig = px.bar(agg_df, x=y_col, y=x_col, color=color, orientation="h", text_auto=True)

    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# LINE CHART
# ══════════════════════════════════════════════════════════════════════════════
elif chart_type == "Line Chart":
    need(num_cols, "numeric")

    x_options = date_cols + num_cols + cat_cols
    need(x_options, "any")
    x_col = st.selectbox("X axis", x_options)

    # Y options exclude X to prevent the duplicate-column ValueError
    y_options = exclude(num_cols, x_col)
    if not y_options:
        st.warning("⚠️ No numeric columns available for Y after removing the X column. "
                   "Please choose a different X axis.")
        st.stop()

    y_cols = st.multiselect("Y axis (numeric — pick one or more)", y_options, default=y_options[:1])
    if not y_cols:
        st.info("👆 Select at least one column for the Y axis.")
        st.stop()

    plot_df = df[[x_col] + y_cols].sort_values(x_col)
    fig = px.line(plot_df, x=x_col, y=y_cols, markers=True)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SCATTER PLOT
# ══════════════════════════════════════════════════════════════════════════════
elif chart_type == "Scatter Plot":
    need(num_cols, "numeric")
    if len(num_cols) < 2:
        st.warning("⚠️ Scatter plot needs at least **2 numeric columns**.")
        st.stop()

    x_col = st.selectbox("X axis (numeric)", num_cols)

    # Y cannot be the same as X
    y_options = exclude(num_cols, x_col)
    y_col = st.selectbox("Y axis (numeric)", y_options)

    # Color: low-cardinality categoricals only — avoids Plotly color crash on numeric/ID cols
    color_options = low_card(cat_cols)
    color = st.selectbox(
        "Color by (optional)",
        ["None"] + color_options,
        help="Only categorical columns with ≤50 unique values are listed."
    )

    # Size: numeric, but not X or Y
    size_options = exclude(num_cols, x_col, y_col)
    size = st.selectbox("Bubble size (optional)", ["None"] + size_options)

    trendline = st.checkbox("Add trendline (OLS)", value=False)

    fig = px.scatter(
        df, x=x_col, y=y_col,
        color=color if color != "None" else None,
        size=size if size != "None" else None,
        trendline="ols" if trendline else None,
        hover_data=df.columns.tolist()
    )
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PIE / DONUT CHART
# ══════════════════════════════════════════════════════════════════════════════
elif chart_type == "Pie / Donut Chart":
    need(num_cols, "numeric")

    # Slices only make sense for low-cardinality categoricals
    label_options = low_card(cat_cols, max_unique=30)
    if not label_options:
        st.warning("⚠️ No categorical column has ≤30 unique values. "
                   "A pie chart with too many slices is unreadable — try a Bar Chart instead.")
        st.stop()

    label_col = st.selectbox("Label column (slice names)", label_options)
    value_col = st.selectbox("Value column (numeric)", num_cols)
    hole = st.slider("Hole size  (0 = Pie,   0.5+ = Donut)", 0.0, 0.7, 0.0, 0.05)

    agg_df = df.groupby(label_col, as_index=False)[value_col].sum()
    fig = px.pie(agg_df, names=label_col, values=value_col, hole=hole)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# HISTOGRAM
# ══════════════════════════════════════════════════════════════════════════════
elif chart_type == "Histogram":
    need(num_cols, "numeric")

    col  = st.selectbox("Column to distribute (numeric)", num_cols)
    bins = st.slider("Number of bins", 5, 100, 20)

    # Color: categoricals only — numeric color causes Plotly to treat it as a gradient, not groups
    color_options = low_card(cat_cols)
    color = st.selectbox(
        "Color by (optional)",
        ["None"] + color_options,
        help="Only categorical columns are listed. "
             "Coloring by a numeric column doesn't make sense for a histogram."
    )

    cumul = st.checkbox("Cumulative", value=False)

    fig = px.histogram(
        df, x=col, nbins=bins,
        color=color if color != "None" else None,
        cumulative=cumul,
        marginal="box"
    )
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# BOX PLOT
# ══════════════════════════════════════════════════════════════════════════════
elif chart_type == "Box Plot":
    need(num_cols, "numeric")

    y_col = st.selectbox("Numeric column (Y axis)", num_cols)

    # Group-by: categoricals only — numeric grouping causes Plotly errors
    group_options = low_card(cat_cols)
    x_col = st.selectbox(
        "Group by (optional)",
        ["None"] + group_options,
        help="Only categorical columns with ≤50 unique values are listed."
    )

    points  = st.selectbox("Show individual points", ["outliers", "all", "suspectedoutliers", False])
    notched = st.checkbox("Notched box", value=False)

    fig = px.box(
        df,
        x=x_col if x_col != "None" else None,
        y=y_col,
        points=points,
        notched=notched
    )
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# AREA CHART
# ══════════════════════════════════════════════════════════════════════════════
elif chart_type == "Area Chart":
    need(num_cols, "numeric")

    x_options = date_cols + num_cols + cat_cols
    need(x_options, "any")
    x_col = st.selectbox("X axis", x_options)

    # Y options exclude X to prevent duplicate-column crash
    y_options = exclude(num_cols, x_col)
    if not y_options:
        st.warning("⚠️ No numeric columns available for Y after removing the X column. "
                   "Please choose a different X axis.")
        st.stop()

    y_cols = st.multiselect("Y columns (numeric)", y_options, default=y_options[:1])
    if not y_cols:
        st.info("👆 Select at least one Y column.")
        st.stop()

    stack = st.checkbox("Stacked area", value=False)

    plot_df = df[[x_col] + y_cols].sort_values(x_col)
    fig = px.area(plot_df, x=x_col, y=y_cols, groupnorm="fraction" if stack else None)
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# HEATMAP (CORRELATION)
# ══════════════════════════════════════════════════════════════════════════════
elif chart_type == "Heatmap (Correlation)":
    need(num_cols, "numeric")
    if len(num_cols) < 2:
        st.warning("⚠️ Need at least **2 numeric columns** to draw a correlation heatmap.")
        st.stop()

    selected = st.multiselect("Columns to include", num_cols, default=num_cols)
    if len(selected) < 2:
        st.info("👆 Select at least 2 columns to compute correlations.")
        st.stop()

    corr = df[selected].corr().round(2)
    fig = go.Figure(
        go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.index.tolist(),
            colorscale="RdBu",
            zmid=0,
            text=corr.values,
            texttemplate="%{text}",
            showscale=True
        )
    )
    fig.update_layout(title="Correlation Matrix", height=max(400, len(selected) * 60))
    st.plotly_chart(fig, use_container_width=True)

# ── download ──────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("💾 Download dataset as CSV"):
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    st.download_button("Download CSV", data=buf.getvalue(),
                       file_name="dataset.csv", mime="text/csv")