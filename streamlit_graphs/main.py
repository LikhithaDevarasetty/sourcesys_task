import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import os

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")
st.title("📊 Superstore Sales — Complete Dashboard")
st.markdown("All charts in one place. Use the sidebar to filter by Region, Segment and Year.")

# ── load data ──────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "train.csv")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  dayfirst=True, errors="coerce")
    df["Month"]      = df["Order Date"].dt.to_period("M").astype(str)
    df["Quarter"]    = df["Order Date"].dt.to_period("Q").astype(str)
    df["Year"]       = df["Order Date"].dt.year
    df["DaysToShip"] = (df["Ship Date"] - df["Order Date"]).dt.days
    return df

uploaded = st.sidebar.file_uploader("Upload a different CSV (optional)", type=["csv", "xlsx"])
if uploaded:
    if uploaded.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded)
    else:
        df = pd.read_csv(uploaded)
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  dayfirst=True, errors="coerce")
    df["Month"]      = df["Order Date"].dt.to_period("M").astype(str)
    df["Quarter"]    = df["Order Date"].dt.to_period("Q").astype(str)
    df["Year"]       = df["Order Date"].dt.year
    df["DaysToShip"] = (df["Ship Date"] - df["Order Date"]).dt.days
else:
    df = load_data(DATA_PATH)

# ── sidebar filters ────────────────────────────────────────────────────────────
st.sidebar.header("Filters")
regions  = st.sidebar.multiselect("Region",  sorted(df["Region"].unique()),  default=sorted(df["Region"].unique()))
segments = st.sidebar.multiselect("Segment", sorted(df["Segment"].unique()), default=sorted(df["Segment"].unique()))
years    = st.sidebar.multiselect("Year",    sorted(df["Year"].unique()),    default=sorted(df["Year"].unique()))

filtered = df[
    df["Region"].isin(regions) &
    df["Segment"].isin(segments) &
    df["Year"].isin(years)
]

if filtered.empty:
    st.warning("No data matches the current filters.")
    st.stop()

PALETTE = ["#4E79A7","#F28E2B","#E15759","#76B7B2","#59A14F",
           "#EDC948","#B07AA1","#FF9DA7","#9C755F","#BAB0AC"]

# ── KPI row ────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Orders",    f"{filtered['Order ID'].nunique():,}")
k2.metric("Total Sales",     f"${filtered['Sales'].sum():,.0f}")
k3.metric("Avg Order Value", f"${filtered.groupby('Order ID')['Sales'].sum().mean():,.0f}")
k4.metric("Cities Covered",  f"{filtered['City'].nunique():,}")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 1 & 2  — bar + pie side by side
# ══════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns([1.4, 1])

with col1:
    st.subheader("1 · Sales by Sub-Category")
    cat_sub = (
        filtered.groupby(["Category","Sub-Category"])["Sales"]
        .sum().reset_index().sort_values("Sales", ascending=True)
    )
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(cat_sub))]
    bars = ax.barh(cat_sub["Sub-Category"], cat_sub["Sales"], color=colors)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 300, bar.get_y() + bar.get_height()/2,
                f"${w/1000:.1f}k", va="center", fontsize=7.5)
    ax.set_xlabel("Sales")
    fig.tight_layout()
    st.pyplot(fig); plt.close(fig)

with col2:
    st.subheader("2 · Sales by Segment")
    seg_sales = filtered.groupby("Segment")["Sales"].sum()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(seg_sales, labels=seg_sales.index, autopct="%1.1f%%",
           startangle=140, colors=PALETTE[:len(seg_sales)],
           wedgeprops=dict(edgecolor="white", linewidth=1.5))
    fig.tight_layout()
    st.pyplot(fig); plt.close(fig)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 3 — monthly line trend
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("3 · Monthly Sales Trend by Region")
monthly = (
    filtered.groupby(["Month","Region"])["Sales"]
    .sum().reset_index().sort_values("Month")
)
fig, ax = plt.subplots(figsize=(14, 4))
for idx, region in enumerate(sorted(monthly["Region"].unique())):
    d = monthly[monthly["Region"] == region]
    ax.plot(d["Month"], d["Sales"], marker="o", markersize=3,
            label=region, color=PALETTE[idx], linewidth=2)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
tick_step = max(1, len(monthly["Month"].unique()) // 12)
ticks = sorted(monthly["Month"].unique())[::tick_step]
ax.set_xticks(ticks)
ax.set_xticklabels(ticks, rotation=45, ha="right", fontsize=8)
ax.legend(title="Region", loc="upper left")
ax.set_ylabel("Sales")
fig.tight_layout()
st.pyplot(fig); plt.close(fig)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 4 & 5 — grouped bar + heatmap
# ══════════════════════════════════════════════════════════════════════════════
col3, col4 = st.columns(2)

with col3:
    st.subheader("4 · Sales by Region & Ship Mode")
    region_ship = (
        filtered.groupby(["Region","Ship Mode"])["Sales"]
        .sum().unstack(fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(7, 4.5))
    region_ship.plot(kind="bar", ax=ax, color=PALETTE[:len(region_ship.columns)],
                     edgecolor="white", linewidth=0.5)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
    ax.set_xticklabels(region_ship.index, rotation=0)
    ax.set_xlabel("")
    ax.set_ylabel("Sales")
    ax.legend(title="Ship Mode", fontsize=8, loc="upper right")
    fig.tight_layout()
    st.pyplot(fig); plt.close(fig)

with col4:
    st.subheader("5 · Category × Region Heatmap")
    pivot = (
        filtered.groupby(["Category","Region"])["Sales"]
        .sum().unstack(fill_value=0)
    )
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.heatmap(pivot/1000, annot=True, fmt=".1f", cmap="YlOrRd",
                linewidths=0.5, linecolor="white", ax=ax,
                cbar_kws={"label": "Sales ($k)"})
    ax.set_xlabel(""); ax.set_ylabel("")
    fig.tight_layout()
    st.pyplot(fig); plt.close(fig)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 6 & 7 — box plot + stacked bar
# ══════════════════════════════════════════════════════════════════════════════
col5, col6 = st.columns(2)

with col5:
    st.subheader("6 · Sales Distribution by Category (Box Plot)")
    categories = sorted(filtered["Category"].unique())
    data_per_cat = [filtered[filtered["Category"] == c]["Sales"].values for c in categories]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bp = ax.boxplot(data_per_cat, patch_artist=True, notch=False,
                    medianprops=dict(color="black", linewidth=1.5))
    for patch, color in zip(bp["boxes"], PALETTE):
        patch.set_facecolor(color); patch.set_alpha(0.8)
    ax.set_xticks(range(1, len(categories)+1))
    ax.set_xticklabels(categories)
    ax.set_ylabel("Sales ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    fig.tight_layout()
    st.pyplot(fig); plt.close(fig)

with col6:
    st.subheader("7 · Yearly Sales by Category (Stacked Bar)")
    yr_cat = (
        filtered.groupby(["Year","Category"])["Sales"]
        .sum().unstack(fill_value=0).sort_index()
    )
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bottom = pd.Series([0]*len(yr_cat), index=yr_cat.index)
    for i, col in enumerate(yr_cat.columns):
        ax.bar(yr_cat.index.astype(str), yr_cat[col], bottom=bottom,
               label=col, color=PALETTE[i], edgecolor="white", linewidth=0.5)
        bottom += yr_cat[col]
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
    ax.set_xlabel("Year"); ax.set_ylabel("Sales")
    ax.legend(title="Category", loc="upper left")
    fig.tight_layout()
    st.pyplot(fig); plt.close(fig)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 8 — sales value histogram
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("8 · Sales Value Distribution (Histogram)")
st.caption("Top 3% clipped for readability. Most orders fall in the low hundreds.")
fig, ax = plt.subplots(figsize=(14, 4))
clipped = filtered["Sales"].clip(upper=filtered["Sales"].quantile(0.97))
ax.hist(clipped, bins=60, color="#4E79A7", edgecolor="white", linewidth=0.4)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
median_val = filtered["Sales"].median()
ax.axvline(median_val, color="#E15759", linewidth=1.5, linestyle="--",
           label=f"Median ${median_val:,.0f}")
ax.set_xlabel("Order Sales Value"); ax.set_ylabel("Number of Orders")
ax.legend()
fig.tight_layout()
st.pyplot(fig); plt.close(fig)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 9 & 10 — violin + stacked segment bar
# ══════════════════════════════════════════════════════════════════════════════
col7, col8 = st.columns(2)

with col7:
    st.subheader("9 · Days to Ship by Shipping Mode (Violin)")
    order_modes = ["Same Day","First Class","Second Class","Standard Class"]
    order_modes = [m for m in order_modes if m in filtered["Ship Mode"].unique()]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    parts = ax.violinplot(
        [filtered[filtered["Ship Mode"] == m]["DaysToShip"].dropna().values for m in order_modes],
        positions=range(len(order_modes)), showmedians=True, showextrema=True
    )
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(PALETTE[i]); pc.set_alpha(0.75)
    parts["cmedians"].set_color("black")
    parts["cmins"].set_color("grey"); parts["cmaxes"].set_color("grey")
    parts["cbars"].set_color("grey")
    ax.set_xticks(range(len(order_modes)))
    ax.set_xticklabels(order_modes, fontsize=9)
    ax.set_ylabel("Days to Ship")
    fig.tight_layout()
    st.pyplot(fig); plt.close(fig)

with col8:
    st.subheader("10 · Orders per Sub-Category by Segment (Stacked Bar)")
    seg_colors = {"Consumer":"#4E79A7","Corporate":"#F28E2B","Home Office":"#59A14F"}
    pivot2 = (
        filtered.groupby(["Sub-Category","Segment"])
        .size().unstack(fill_value=0)
        .sort_values(filtered["Segment"].value_counts().index[0], ascending=True)
    )
    fig, ax = plt.subplots(figsize=(7, 5))
    left = pd.Series([0]*len(pivot2), index=pivot2.index)
    for seg in pivot2.columns:
        ax.barh(pivot2.index, pivot2[seg], left=left,
                label=seg, color=seg_colors.get(seg, "#BAB0AC"),
                edgecolor="white", linewidth=0.4)
        left += pivot2[seg]
    ax.set_xlabel("Number of Orders")
    ax.legend(title="Segment", loc="lower right")
    fig.tight_layout()
    st.pyplot(fig); plt.close(fig)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 11 — bubble chart (top 20 states)
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("11 · State Performance Bubble Chart (Top 20 States)")
st.caption("X = orders, Y = total sales, bubble size = avg sale value per order.")
state_stats = (
    filtered.groupby("State")
    .agg(total_sales=("Sales","sum"), order_count=("Order ID","count"), avg_sale=("Sales","mean"))
    .reset_index().sort_values("total_sales", ascending=False).head(20)
)
fig, ax = plt.subplots(figsize=(13, 5))
sc = ax.scatter(state_stats["order_count"], state_stats["total_sales"],
                s=state_stats["avg_sale"]*2.5, c=state_stats["total_sales"],
                cmap="YlOrRd", alpha=0.85, edgecolors="white", linewidths=0.6)
for _, row in state_stats.iterrows():
    ax.annotate(row["State"], (row["order_count"], row["total_sales"]),
                fontsize=7.5, ha="center", va="bottom", xytext=(0,5),
                textcoords="offset points")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
ax.set_xlabel("Number of Orders"); ax.set_ylabel("Total Sales")
fig.colorbar(sc, ax=ax, pad=0.01).set_label("Total Sales ($)")
fig.tight_layout()
st.pyplot(fig); plt.close(fig)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 12 — stacked area (quarterly by category)
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("12 · Quarterly Sales by Category (Stacked Area)")
qtr_cat = (
    filtered.groupby(["Quarter","Category"])["Sales"]
    .sum().unstack(fill_value=0).sort_index()
)
fig, ax = plt.subplots(figsize=(14, 4.5))
baseline = np.zeros(len(qtr_cat))
x = range(len(qtr_cat))
for i, cat in enumerate(qtr_cat.columns):
    vals = qtr_cat[cat].values
    ax.fill_between(x, baseline, baseline+vals, label=cat, color=PALETTE[i], alpha=0.8)
    baseline += vals
tick_step = max(1, len(qtr_cat)//10)
ax.set_xticks(list(x)[::tick_step])
ax.set_xticklabels(qtr_cat.index[::tick_step], rotation=45, ha="right", fontsize=8)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
ax.set_ylabel("Sales"); ax.legend(loc="upper left")
fig.tight_layout()
st.pyplot(fig); plt.close(fig)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 13 — lollipop (top 15 customers)
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("13 · Top 15 Customers by Total Sales (Lollipop)")
top_customers = (
    filtered.groupby("Customer Name")["Sales"]
    .sum().sort_values(ascending=True).tail(15).reset_index()
)
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.hlines(top_customers["Customer Name"], 0, top_customers["Sales"],
          color="#B0BEC5", linewidth=1.5)
ax.scatter(top_customers["Sales"], top_customers["Customer Name"],
           color="#4E79A7", s=80, zorder=3)
for _, row in top_customers.iterrows():
    ax.text(row["Sales"]+300, row["Customer Name"],
            f"${row['Sales']:,.0f}", va="center", fontsize=8)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
ax.set_xlabel("Total Sales")
ax.set_xlim(0, top_customers["Sales"].max()*1.18)
fig.tight_layout()
st.pyplot(fig); plt.close(fig)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 14 — calendar heatmap (most recent year)
# ══════════════════════════════════════════════════════════════════════════════
st.subheader("14 · Daily Order Activity Calendar (Most Recent Year)")
st.caption("Each cell is one day. Darker = more orders placed that day.")
latest_year = int(filtered["Year"].max())
cal_df = filtered[filtered["Year"] == latest_year].copy()
cal_df["date"] = cal_df["Order Date"].dt.date
cal_counts = cal_df.groupby("date").size().reset_index()
cal_counts.columns = ["date","count"]
cal_counts["date"]    = pd.to_datetime(cal_counts["date"])
cal_counts["week"]    = cal_counts["date"].dt.isocalendar().week.astype(int)
cal_counts["weekday"] = cal_counts["date"].dt.weekday

grid = np.zeros((53, 7))
for _, row in cal_counts.iterrows():
    w = int(row["week"]) - 1
    d = int(row["weekday"])
    if 0 <= w < 53:
        grid[w][d] = row["count"]

fig, ax = plt.subplots(figsize=(14, 3.5))
im = ax.imshow(grid.T, aspect="auto", cmap="Blues", interpolation="nearest")
ax.set_yticks(range(7))
ax.set_yticklabels(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], fontsize=8)
month_starts, month_labels = [], []
for month in range(1, 13):
    first_day = pd.Timestamp(f"{latest_year}-{month:02d}-01")
    w = int(first_day.isocalendar().week) - 1
    if w not in month_starts:
        month_starts.append(w)
        month_labels.append(first_day.strftime("%b"))
ax.set_xticks(month_starts)
ax.set_xticklabels(month_labels, fontsize=8)
ax.set_xlabel(f"Week of {latest_year}")
fig.colorbar(im, ax=ax, orientation="vertical", label="Orders/day", pad=0.01)
fig.tight_layout()
st.pyplot(fig); plt.close(fig)

# ── raw data viewer ────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("🗂 View Filtered Raw Data"):
    st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
    st.caption(f"{len(filtered):,} rows shown")